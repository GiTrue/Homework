# stations/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator
import csv
import os
from urllib.parse import urlencode # Для создания ссылок с параметром 'page'


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # 1. Чтение CSV-файла
    file_path = settings.BUS_STATION_CSV
    stations_list = []
    
    # Используем DictReader и кодировку utf-8 для чтения данных
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            # Пропускаем первые две строки с метаданными, если они есть
            # (судя по сниппету, файл начинается с метаданных)
            for _ in range(2):
                next(csvfile) 
                
            reader = csv.DictReader(csvfile, delimiter=';') # Используем точку с запятой как разделитель
            for row in reader:
                stations_list.append(row)
                
    except FileNotFoundError:
        # Если файл не найден, список останется пустым
        pass
    except Exception as e:
        # Для отладки, если возникнет другая ошибка чтения
        print(f"Error reading CSV: {e}")
        pass

    # 2. Пагинация
    PER_PAGE = 10 # Задаем количество элементов на страницу
    paginator = Paginator(stations_list, PER_PAGE)
    
    # Получаем номер страницы из GET-параметра 'page'. По умолчанию - 1
    current_page_number = request.GET.get('page', 1)
    
    try:
        # Получаем объект Page для текущей страницы
        page = paginator.page(current_page_number)
    except Exception:
        # Если номер страницы невалиден, берем первую или последнюю
        page = paginator.page(1)
    
    # 3. Формирование ссылок для навигации
    prev_page_url = None
    next_page_url = None
    
    # Базовый URL для маршрута 'bus_stations'
    base_url = reverse('bus_stations')
    
    if page.has_next():
        next_page_number = page.next_page_number()
        # Формируем URL с параметром page
        next_page_url = f'{base_url}?{urlencode({"page": next_page_number})}'
    
    if page.has_previous():
        prev_page_number = page.previous_page_number()
        prev_page_url = f'{base_url}?{urlencode({"page": prev_page_number})}'

    # 4. Формирование контекста
    context = {
        'bus_stations': page.object_list,    # Список остановок на текущей странице
        'page': page,                       # Объект Page (полезен для has_next/has_previous)
        'current_page': page.number,        # Текущий номер страницы
        'prev_page_url': prev_page_url,     # Ссылка для кнопки "Назад"
        'next_page_url': next_page_url,     # Ссылка для кнопки "Вперед"
    }
    
    return render(request, 'stations/index.html', context)
