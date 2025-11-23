from django.db import models
from django.utils.text import slugify


class Phone(models.Model):
    # Устанавливаем id как основной ключ
    id = models.IntegerField(primary_key=True)
    
    name = models.CharField(max_length=100, verbose_name='Название')
    price = models.IntegerField(verbose_name='Цена')
    image = models.URLField(verbose_name='Изображение')
    release_date = models.DateField(verbose_name='Дата выпуска')
    lte_exists = models.BooleanField(verbose_name='Поддержка LTE')
    # Slug нужен для красивых URL. Должен быть уникальным, но slugify не гарантирует этого.
    # В рамках задания, сделаем его просто CharField.
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Автоматически генерируем slug из поля name при сохранении
        # Slugify преобразует "Iphone X" в "iphone-x"
        if not self.slug:
            self.slug = slugify(self.name)
        super(Phone, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'
