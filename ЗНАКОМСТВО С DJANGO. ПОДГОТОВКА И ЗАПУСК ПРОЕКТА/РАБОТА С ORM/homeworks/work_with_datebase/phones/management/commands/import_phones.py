import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from phones.models import Phone
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Imports phone data from phones.csv into the database'

    def handle(self, *args, **options):       
        csv_file_path = os.path.join(settings.BASE_DIR.parent, 'phones.csv')
        
        # Очищаем таблицу перед импортом, чтобы избежать дубликатов
        Phone.objects.all().delete()
        
        self.stdout.write(self.style.NOTICE(f'Reading data from: {csv_file_path}'))

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                # Используем ; как разделитель, как в файле phones.csv
                phones = list(csv.DictReader(file, delimiter=';'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {csv_file_path}'))
            return
            
        objects_to_create = []

        for phone in phones:
            # Преобразуем строковые значения в нужные типы
            
            # release_date: "2016-12-12" -> date object
            try:
                release_date_obj = datetime.strptime(phone['release_date'], '%Y-%m-%d').date()
            except ValueError:
                self.stdout.write(self.style.WARNING(f"Skipping phone with invalid date: {phone['name']}"))
                continue

            # lte_exists: "True" / "False" -> boolean
            lte_bool = phone['lte_exists'].lower() == 'true'

            # Создаем объект Phone, который будет сохранен позже
            objects_to_create.append(
                Phone(
                    id=int(phone['id']),
                    name=phone['name'],
                    image=phone['image'],
                    price=int(phone['price']),
                    release_date=release_date_obj,
                    lte_exists=lte_bool,
                    # Поле slug будет заполнено автоматически в методе save()
                )
            )

        # Используем bulk_create для эффективной массовой вставки
        Phone.objects.bulk_create(objects_to_create)
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(objects_to_create)} phones.'))
