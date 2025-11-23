from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Book


def books_view(request, date=None):
    template = 'books/books_list.html'
    
    if date is None:
        # Если дата не передана (маршрут /books/), показываем все книги
        book_list = Book.objects.all().order_by('pub_date')
        prev_date_url = None
        next_date_url = None
    else:
        # Если дата передана (маршрут /books/ГГГГ-ММ-ДД/)
        
        # 1. Фильтруем книги по переданной дате
        book_list = Book.objects.filter(pub_date=date).order_by('name')

        # 2. Находим следующую и предыдущую уникальные даты публикации
        
        # Предыдущая дата: ищем максимальную дату, которая меньше текущей
        prev_book = Book.objects.filter(pub_date__lt=date).order_by('-pub_date').first()
        if prev_book:
            prev_date = prev_book.pub_date
            # Формируем URL для предыдущей даты
            prev_date_url = reverse('books_by_date', kwargs={'date': prev_date})
        else:
            prev_date_url = None

        # Следующая дата: ищем минимальную дату, которая больше текущей
        next_book = Book.objects.filter(pub_date__gt=date).order_by('pub_date').first()
        if next_book:
            next_date = next_book.pub_date
            # Формируем URL для следующей даты
            next_date_url = reverse('books_by_date', kwargs={'date': next_date})
        else:
            next_date_url = None

    context = {
        'books': book_list,
        'date': date, # Передаем текущую дату, если она есть
        'prev_date_url': prev_date_url,
        'next_date_url': next_date_url,
    }
    return render(request, template, context)
