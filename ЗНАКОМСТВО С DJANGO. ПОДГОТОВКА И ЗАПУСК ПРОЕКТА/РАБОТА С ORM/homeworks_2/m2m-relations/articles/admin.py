from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormSet(BaseInlineFormSet):
    """
    Кастомный формсет для проверки условия: 
    должен быть выбран один и только один основной раздел (is_main=True).
    """
    def clean(self):
        # Проверяем, что базовый метод clean отработал
        super().clean() 

        main_count = 0
        
        # Перебираем все формы, которые будут сохранены (т.е. не помечены на удаление)
        for form in self.forms:
            # Проверяем, что форма содержит данные и не помечена на удаление
            if form.cleaned_data.get('DELETE') or not form.cleaned_data:
                continue

            # Считаем количество основных разделов
            if form.cleaned_data.get('is_main'):
                main_count += 1
        
        # Проверка условия "один и только один основной раздел"
        if main_count == 0:
            raise ValidationError('Необходимо выбрать **хотя бы один** основной раздел.')
        if main_count > 1:
            raise ValidationError('Основным может быть выбран **только один** раздел.')


class ScopeInline(admin.TabularInline):
    """
    Inline для отображения и редактирования связей Scope на странице Article.
    """
    model = Scope
    formset = ScopeInlineFormSet # Используем наш кастомный формсет для валидации
    extra = 0 # Не добавлять пустых форм по умолчанию, только те, что уже есть


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    # Отображение для управления разделами
    list_display = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # Добавление Inline для редактирования разделов
    inlines = [ScopeInline]
    list_display = ('title', 'published_at',) # Добавим для удобства
    list_filter = ('published_at',)
