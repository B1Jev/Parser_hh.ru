import requests
from parser_app.models import Vacancy

def parse_hh(query):
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": query,
        "area": 1,  # Москва
        "per_page": 100  # макс количество на страницу
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, params=params, headers=headers)
    print(f"Status code: {response.status_code}")
    
    data = response.json()
    print("Структура ответа API:")
    print(data)

    if response.status_code != 200:
        print(f"Ошибка API: {data.get('description', 'Описание ошибки отсутствует')}")
        print(f"Детали ошибки: {data.get('errors', 'Детали отсутствуют')}")
        return []

    total_found = data.get('found', 'Не указано')
    print(f"Total vacancies found: {total_found}")
    
    results = []
    items = data.get('items', [])
    for item in items:
        title = item.get('name', 'Название не указано')
        company = item.get('employer', {}).get('name', 'Компания не указана')
        description = item.get('snippet', {}).get('requirement', 'Описание не указано')
        salary = 'Не указана'
        if item.get('salary'):
            from_salary = item['salary'].get('from', '')
            to_salary = item['salary'].get('to', '')
            currency = item['salary'].get('currency', '')
            if from_salary and to_salary:
                salary = f"{from_salary} - {to_salary} {currency}"
            elif from_salary:
                salary = f"от {from_salary} {currency}"
            elif to_salary:
                salary = f"до {to_salary} {currency}"
        
        url = item.get('alternate_url', '#')
        
        vacancy_obj = Vacancy.objects.create(
            title=title,
            company=company,
            description=description,
            salary=salary,
            url=url,
            source='hh.ru'
        )
        results.append(vacancy_obj)
    
    print(f"Number of vacancies processed: {len(results)}")
    return results