import pytest
from rest_framework.test import APIClient
from model_bakery import baker


@pytest.fixture
def api_client():
    """Фикстура для API клиента DRF."""
    return APIClient()


@pytest.fixture
def course_factory():
    """Фикстура для фабрики курсов (использует model_bakery)."""
    def factory(*args, **kwargs):
        return baker.make('students.Course', *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    """Фикстура для фабрики студентов (использует model_bakery)."""
    def factory(*args, **kwargs):
        return baker.make('students.Student', *args, **kwargs)
    return factory