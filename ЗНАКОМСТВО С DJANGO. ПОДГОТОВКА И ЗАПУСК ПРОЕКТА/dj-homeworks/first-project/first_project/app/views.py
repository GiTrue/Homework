from django.http import HttpResponse
from django.shortcuts import render, reverse
from datetime import datetime
import os  # Импортируем os для workdir_view


def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        # Используем 'time' и 'workdir' как имена URL-путей
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }

    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    # обратите внимание – здесь HTML шаблона нет, 
    # возвращается просто текст
    # Получаем текущее время
    current_time = datetime.now().strftime('%H:%M:%S')
    msg = f'Текущее время: {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    # по аналогии с `time_view`, напишите код,
    # который возвращает список файлов в рабочей
    # директории
    # Получаем список файлов в текущей директории
    files = os.listdir(os.getcwd())

    # Форматируем список в HTML (например, как список)
    list_items = [f'<li>{file}</li>' for file in files]
    list_html = '\n'.join(list_items)

    html_content = f'<h1>Содержимое рабочей директории:</h1><ul>{list_html}</ul>'

    return HttpResponse(html_content)
