# books/admin.py

from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'pub_date')
    # Добавляем фильтр по дате публикации
    list_filter = ('pub_date',)
    ordering = ('pub_date',)
