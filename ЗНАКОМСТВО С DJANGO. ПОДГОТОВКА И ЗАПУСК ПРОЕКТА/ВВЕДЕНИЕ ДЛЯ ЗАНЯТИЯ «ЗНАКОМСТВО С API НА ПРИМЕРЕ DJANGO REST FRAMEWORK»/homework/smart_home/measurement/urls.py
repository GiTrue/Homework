from django.urls import path

from .views import (
    SensorListCreate,
    SensorRetrieveUpdate,
    MeasurementCreate
)

urlpatterns = [
    # Список датчиков и создание датчика
    path('sensors/', SensorListCreate.as_view(), name='sensor-list-create'),
    # Информация о конкретном датчике и его обновление
    path('sensors/<int:pk>/', SensorRetrieveUpdate.as_view(), name='sensor-retrieve-update'),
    # Добавление измерения
    path('measurements/', MeasurementCreate.as_view(), name='measurement-create'),
]