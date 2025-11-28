from django.urls import path

# Импортируем вашу view-функцию
from .views import articles_list 

urlpatterns = [
    # Главная страница вашего приложения будет обрабатываться функцией articles_list
    path('', articles_list, name='articles'),
]
