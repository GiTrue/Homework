from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q # Импортируем Q для сложного поиска

from .models import Product, Stock
from .serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # при необходимости добавьте параметры фильтрации
    
    # 3. Реализация поиска
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']
    
    # 4. Настройка пагинации
    pagination_class = LimitOffsetPagination


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    # при необходимости добавьте параметры фильтрации

    # 3. Реализация фильтрации и поиска (для дополнительного задания)
    filter_backends = [SearchFilter, OrderingFilter]
    
    # Дополнительное задание: поиск складов, в которых есть продукт по названию/описанию продукта
    # Используем SearchFilter, но переопределяем queryset для работы с поиском по связанным полям.
    # search_fields здесь не используется, т.к. мы переопределяем get_queryset
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        
        if search_query:
            # Фильтрация складов, которые содержат продукт,
            # где название ИЛИ описание продукта содержит строку поиска
            queryset = queryset.filter(
                Q(products__title__icontains=search_query) |
                Q(products__description__icontains=search_query)
            ).distinct()
            
        return queryset

    # 4. Настройка пагинации
    pagination_class = LimitOffsetPagination
