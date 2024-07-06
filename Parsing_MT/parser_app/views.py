from django.shortcuts import render
from .parsers import hh_parser  

def index(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        vacancies = hh_parser.parse_hh(keyword)
        return render(request, 'results.html', {
            'vacancies': vacancies,
            'keyword': keyword
        })
    return render(request, 'index.html')