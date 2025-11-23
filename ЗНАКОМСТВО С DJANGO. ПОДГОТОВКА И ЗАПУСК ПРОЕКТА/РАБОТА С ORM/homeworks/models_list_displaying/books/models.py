# coding=utf-8

from django.db import models


class Book(models.Model):
    name = models.CharField('Название', max_length=64)
    author = models.CharField('Автор', max_length=64)
    # Используем DateField для даты публикации
    pub_date = models.DateField('Дата публикации')

    def __str__(self):
        return f"{self.name} ({self.author})"
    
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        # Сортируем по дате публикации по возрастанию по умолчанию
        ordering = ['pub_date']
