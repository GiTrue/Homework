import pytest
from rest_framework import status
from django.urls import reverse

@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    # Создаем курс через фабрику
    course = course_factory()
    
    # Делаем запрос
    url = reverse('courses-detail', args=[course.id])
    response = api_client.get(url)
    
    # Проверка
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == course.id
    assert response.data['name'] == course.name

@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    # Создаем курсы
    courses = course_factory(_quantity=10)
    
    # Запрос списка
    url = reverse('courses-list')
    response = api_client.get(url)
    
    # Проверка
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == len(courses)
    for i, course in enumerate(courses):
        assert response.data[i]['name'] == course.name

@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    # Создаем несколько курсов
    courses = course_factory(_quantity=5)
    target_course = courses[2]
    
    # Фильтруем по ID
    url = reverse('courses-list')
    response = api_client.get(url, data={'id': target_course.id})
    
    # Проверка
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['id'] == target_course.id

@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    # Создаем несколько курсов
    courses = course_factory(_quantity=5)
    target_course = courses[3]
    
    # Фильтруем по имени
    url = reverse('courses-list')
    response = api_client.get(url, data={'name': target_course.name})
    
    # Проверка
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == target_course.name

@pytest.mark.django_db
def test_create_course(api_client):
    # Данные для создания
    payload = {'name': 'Python Developer'}
    
    # POST запрос
    url = reverse('courses-list')
    response = api_client.post(url, data=payload)
    
    # Проверка
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == payload['name']

@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    # Создаем курс
    course = course_factory()
    payload = {'name': 'Updated Course Name'}
    
    # PATCH запрос
    url = reverse('courses-detail', args=[course.id])
    response = api_client.patch(url, data=payload)
    
    # Проверка
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == payload['name']

@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    # Создаем курс
    course = course_factory()
    
    # DELETE запрос
    url = reverse('courses-detail', args=[course.id])
    response = api_client.delete(url)
    
    # Проверка
    assert response.status_code == status.HTTP_204_NO_CONTENT

# --- ТЕСТ ДЛЯ ДОПОЛНИТЕЛЬНОГО ЗАДАНИЯ ---
@pytest.mark.django_db
@pytest.mark.parametrize(
    "students_count, expected_status",
    [
        (20, status.HTTP_201_CREATED),     # Успешно (граница)
        (21, status.HTTP_400_BAD_REQUEST), # Ошибка (превышение)
    ]
)
def test_max_students_per_course(api_client, student_factory, settings, students_count, expected_status):
    # Фиксируем лимит в настройках через фикстуру settings
    settings.MAX_STUDENTS_PER_COURSE = 20
    
    # Создаем нужное количество студентов
    students = student_factory(_quantity=students_count)
    student_ids = [s.id for s in students]
    
    # Пытаемся создать курс с этими студентами
    url = reverse('courses-list')
    payload = {
        'name': 'Test Validation Course',
        'students': student_ids
    }
    response = api_client.post(url, data=payload)
    
    # Проверка результата
    assert response.status_code == expected_status