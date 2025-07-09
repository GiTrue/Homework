Задание № 4. Полевые испытания
Создайте по 2 экземпляра каждого класса, вызовите все созданные методы, а также реализуйте две функции:

для подсчета средней оценки за домашние задания по всем студентам в рамках конкретного курса (в качестве аргументов принимаем список студентов и название курса);
для подсчета средней оценки за лекции всех лекторов в рамках курса (в качестве аргумента принимаем список лекторов и название курса).


# Классы

class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            lecturer.grades.setdefault(course, []).append(grade)
        else:
            return 'Ошибка'

    def average_grade(self):
        total = 0
        count = 0
        for course_grades in self.grades.values():
            total += sum(course_grades)
            count += len(course_grades)
        return total / count if count > 0 else 0

    def __str__(self):
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за домашние задания: {self.average_grade():.1f}\n"
            f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n"
            f"Завершенные курсы: {', '.join(self.finished_courses)}"
        )

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() < other.average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def average_grade(self):
        total = 0
        count = 0
        for course_grades in self.grades.values():
            total += sum(course_grades)
            count += len(course_grades)
        return total / count if count > 0 else 0

    def __str__(self):
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за лекции: {self.average_grade():.1f}"
        )

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() < other.average_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            student.grades.setdefault(course, []).append(grade)
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


# Функции подсчёта средней оценки 

def average_hw_grade(students, course):
    total = 0
    count = 0
    for student in students:
        if course in student.grades:
            total += sum(student.grades[course])
            count += len(student.grades[course])
    return total / count if count > 0 else 0


def average_lecture_grade(lecturers, course):
    total = 0
    count = 0
    for lecturer in lecturers:
        if course in lecturer.grades:
            total += sum(lecturer.grades[course])
            count += len(lecturer.grades[course])
    return total / count if count > 0 else 0


# Создание объектов

# Студенты
student1 = Student('Алиса', 'Белая', 'ж')
student2 = Student('Борис', 'Краснов', 'м')

student1.courses_in_progress += ['Python', 'Git']
student1.finished_courses += ['Введение в программирование']

student2.courses_in_progress += ['Python', 'Java']
student2.finished_courses += ['ООП']

# Лекторы
lecturer1 = Lecturer('Иван', 'Иванов')
lecturer2 = Lecturer('Анна', 'Смирнова')

lecturer1.courses_attached += ['Python']
lecturer2.courses_attached += ['Python', 'Java']

# Проверяющие
reviewer1 = Reviewer('Мария', 'Коваль')
reviewer2 = Reviewer('Сергей', 'Петров')

reviewer1.courses_attached += ['Python', 'Java']
reviewer2.courses_attached += ['Git', 'Python']

# Оценки 

# Лекторам от студентов
student1.rate_lecture(lecturer1, 'Python', 9)
student1.rate_lecture(lecturer1, 'Python', 10)
student2.rate_lecture(lecturer1, 'Python', 8)

student2.rate_lecture(lecturer2, 'Java', 7)
student2.rate_lecture(lecturer2, 'Python', 9)

# Студентам от проверяющих
reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student2, 'Python', 7)
reviewer1.rate_hw(student2, 'Java', 8)
reviewer2.rate_hw(student1, 'Git', 9)

# Вывод объектов 

print(student1, '\n')
print(student2, '\n')
print(lecturer1, '\n')
print(lecturer2, '\n')
print(reviewer1, '\n')
print(reviewer2, '\n')

# Сравнение

print(f"Студент лучше: {student1.surname if student1 > student2 else student2.surname}")
print(f"Лектор лучше: {lecturer1.surname if lecturer1 > lecturer2 else lecturer2.surname}\n")

# Средние оценки по курсу

students = [student1, student2]
lecturers = [lecturer1, lecturer2]

print(f"Средняя оценка за ДЗ по Python: {average_hw_grade(students, 'Python'):.1f}")
print(f"Средняя оценка за ДЗ по Java: {average_hw_grade(students, 'Java'):.1f}")
print(f"Средняя оценка за лекции по Python: {average_lecture_grade(lecturers, 'Python'):.1f}")
print(f"Средняя оценка за лекции по Java: {average_lecture_grade(lecturers, 'Java'):.1f}")