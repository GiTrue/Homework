# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView

from .models import Sensor, Measurement
from .serializers import (
    SensorListSerializer,
    SensorDetailSerializer,
    MeasurementSerializer
)


class SensorListCreate(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorListSerializer


class SensorRetrieveUpdate(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer


class MeasurementCreate(CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def perform_create(self, serializer):
        # Получаем ID датчика из данных запроса
        sensor_id = self.request.data.get('sensor')
        # Получаем объект Sensor
        sensor = Sensor.objects.get(id=sensor_id)
        # Создаем новое измерение, связывая его с датчиком
        serializer.save(sensor=sensor)