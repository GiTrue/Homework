from django.conf import settings
from rest_framework import serializers

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate_students(self, value):
        """
        Дополнительное задание: валидация максимального числа студентов на курсе.
        """
        # Проверяем количество переданных ID студентов
        if len(value) > settings.MAX_STUDENTS_PER_COURSE:
            raise serializers.ValidationError(
                f"Количество студентов на курсе не может превышать {settings.MAX_STUDENTS_PER_COURSE}."
            )
        return value