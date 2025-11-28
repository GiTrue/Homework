from django.shortcuts import render

from .models import Article # Импортируем Article из текущего приложения


def articles_list(request):
    template = 'articles/news.html'

    # 1. Получаем все статьи.
    # 2. Используем prefetch_related для предварительной загрузки (оптимизации)
    #    связей 'scopes' (Scope) и 'scopes__tag' (Tag), чтобы избежать N+1 запросов.
    # 3. Сортировка статей по дате (-published_at) уже определена в Article.Meta.
    # 4. Связанные Scope (article.scopes.all) будут автоматически отсортированы
    #    согласно Scope.Meta.ordering = ['-is_main', 'tag__name']
    articles = Article.objects.prefetch_related('scopes', 'scopes__tag').all()

    context = {
        # В шаблоне используется 'object_list'
        'object_list': articles
    }

    return render(request, template, context)
