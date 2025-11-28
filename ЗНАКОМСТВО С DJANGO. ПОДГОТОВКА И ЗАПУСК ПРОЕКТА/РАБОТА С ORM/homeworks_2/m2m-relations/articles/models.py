from django.db import models
from django.db.models import UniqueConstraint


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название раздела', unique=True)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        # Сортировка по имени, чтобы соответствовать второму условию сортировки
        ordering = ['name'] 

    def __str__(self):
        return self.name

class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)
    
    # Явная связь многие-ко-многим через промежуточную модель Scope
    tags = models.ManyToManyField(Tag, through='Scope', verbose_name='Разделы')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

class Scope(models.Model):
    # related_name='scopes' соответствует вызову article.scopes.all в шаблоне
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes', verbose_name='Статья')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Раздел')
    is_main = models.BooleanField(default=False, verbose_name='Основной')

    class Meta:
        verbose_name = 'Тематика статьи'
        verbose_name_plural = 'Тематики статьи'
        # Сортировка для шаблона: сначала основной тег (True > False), потом остальные по имени тега (алфавит)
        ordering = ['-is_main', 'tag__name']
        # Гарантируем, что для одной статьи один тег может быть использован только один раз
        UniqueConstraint(fields=['article', 'tag'], name='unique_article_tag')

    def __str__(self):
        return f'{self.article.title} - {self.tag.name}'
