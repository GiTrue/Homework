# calculator/views.py
from django.shortcuts import render

# Источник данных для рецептов
DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

def recipe_view(request, dish_name):
    # 1. Получаем базовый рецепт по имени блюда
    # Если блюдо не найдено, 'recipe' будет None
    recipe = DATA.get(dish_name)
    
    # Инициализируем контекст
    context = {'recipe': None}
    
    if recipe:
        # 2. Получаем опциональный параметр servings
        servings_str = request.GET.get('servings', '1') # По умолчанию 1 порция
        
        try:
            # Преобразуем servings в целое число
            servings = int(servings_str)
            # Убеждаемся, что число порций положительное
            if servings <= 0:
                servings = 1
        except ValueError:
            # Если servings не является числом, используем 1 порцию
            servings = 1
        
        # 3. Рассчитываем рецепт на нужное количество порций
        calculated_recipe = {}
        for ingredient, amount in recipe.items():
            # Умножаем количество ингредиента на число порций
            calculated_recipe[ingredient] = amount * servings
            
        # 4. Формируем контекст для шаблона
        context['recipe'] = calculated_recipe

    # Используем шаблон index.html из папки calculator (как предполагает apps.py)
    return render(request, 'calculator/index.html', context)

