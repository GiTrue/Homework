"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, register_converter

# Импортируем конвертер и представление
from books.views import books_view
from books.converters import DateConverter

# Регистрируем конвертер
register_converter(DateConverter, 'pub_date')

urlpatterns = [
    # 1. Список всех книг
    path('books/', books_view, name='books'),
    
    # 2. Список книг по конкретной дате: /books/2021-01-02/
    path('books/<pub_date:date>/', books_view, name='books_by_date'),
    
    path('admin/', admin.site.urls),
]