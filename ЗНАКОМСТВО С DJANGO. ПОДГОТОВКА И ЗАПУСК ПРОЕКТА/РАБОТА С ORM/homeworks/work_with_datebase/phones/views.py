from django.shortcuts import render, redirect, get_object_or_404
from .models import Phone

def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    
    # Получаем параметр сортировки из GET-запроса
    sort_param = request.GET.get('sort')
    
    phones = Phone.objects.all()
    
    if sort_param == 'name':
        # Сортировка по названию (алфавитный порядок)
        phones = phones.order_by('name')
    elif sort_param == 'min_price':
        # Сортировка по цене (по возрастанию)
        phones = phones.order_by('price')
    elif sort_param == 'max_price':
        # Сортировка по цене (по убыванию)
        phones = phones.order_by('-price')

    context = {
        'phones': phones,
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    
    # Используем get_object_or_404 для получения продукта или ошибки 404
    phone = get_object_or_404(Phone, slug=slug)
    
    context = {
        'phone': phone,
    }
    return render(request, template, context)
