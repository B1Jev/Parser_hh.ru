from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import os
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    host=os.environ.get("POSTGRES_HOST", "db"),
    database=os.environ.get("POSTGRES_DB", "hh_parser"),
    user=os.environ.get("POSTGRES_USER", "postgres"),
    password=os.environ.get("POSTGRES_PASSWORD", "postgres")
)
cursor = conn.cursor()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        keyword = request.form.get("keyword")
        city = request.form.get("city")
        vacancies = parse_hh_vacancies(keyword, city, pages=1)

        for vacancy in vacancies:
            cursor.execute(
                "INSERT INTO vacancies (title, company, url) VALUES (%s, %s, %s)",
                (vacancy['title'], vacancy['company'], vacancy['url'])
            )
        conn.commit()

        return render_template("results.html", vacancies=vacancies)
    return render_template("index.html")

def parse_hh_vacancies(keyword, city, pages=1):
  """Парсит вакансии на HH.ru

  Args:
    keyword: Ключевое слово для поиска вакансий
    city: Город для поиска вакансий
    pages: Количество страниц для парсинга (по умолчанию 1)

  Returns:
    Список словарей с данными о вакансиях
  """
  vacancies = []
  for page in range(1, pages + 1):
    search_url = f"https://hh.ru/search/vacancy"
    response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0'})

    if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')
      vacancy_elements = soup.select(".vacancy-serp-item")

      for vacancy_element in vacancy_elements:
        title = vacancy_element.select_one(".vacancy-serp-item__title").text.strip()
        company = vacancy_element.select_one(".vacancy-serp-item__company").text.strip()
        url = vacancy_element.select_one(".vacancy-serp-item__title a")['href']
        vacancies.append({'title': title, 'company': company, 'url': url})

  return vacancies

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')