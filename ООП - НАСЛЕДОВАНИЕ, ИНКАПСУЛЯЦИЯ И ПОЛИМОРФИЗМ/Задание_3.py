Задание № 3. Полиморфизм и магические методы

Перегрузите магический метод __str__ у всех классов.
У проверяющих он должен выводить информацию в следующем виде:

print(some_reviewer)
Имя: Some
Фамилия: Buddy

У лекторов:

print(some_lecturer)
Имя: Some
Фамилия: Buddy
Средняя оценка за лекции: 9.9

А у студентов так:

print(some_student)
Имя: Ruoy
Фамилия: Eman
Средняя оценка за домашние задания: 9.9
Курсы в процессе изучения: Python, Git
Завершенные курсы: Введение в программирование

Реализуйте возможность сравнивать (через операторы сравнения) между собой лекторов по средней оценке за лекции и студентов по средней оценке за домашние задания.


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer) and
            course in self.courses_in_progress and
            course in lecturer.courses_attached):
            lecturer.grades.setdefault(course, []).append(grade)
        else:
            return 'Ошибка'

    def average_grade(self):
        total = 0
        count = 0
        for grades in self.grades.values():
            total += sum(grades)
            count += len(grades)
        return total / count if count > 0 else 0

    def __str__(self):
        avg = self.average_grade()
        in_progress = ', '.join(self.courses_in_progress)
        finished = ', '.join(self.finished_courses)
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {avg:.1f}\n'
                f'Курсы в процессе изучения: {in_progress}\n'
                f'Завершенные курсы: {finished}')

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
        for grades in self.grades.values():
            total += sum(grades)
            count += len(grades)
        return total / count if count > 0 else 0

    def __str__(self):
        avg = self.average_grade()
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за лекции: {avg:.1f}')

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() < other.average_grade()

class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if (isinstance(student, Student) and
            course in self.courses_attached and
            course in student.courses_in_progress):
            student.grades.setdefault(course, []).append(grade)
        else:
            return 'Ошибка'

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


Пример использования:

student1 = Student('Ольга', 'Алёхина', 'ж')
student1.courses_in_progress += ['Python', 'Git']
student1.finished_courses += ['Введение в программирование']

student2 = Student('Виктор', 'Котов', 'м')
student2.courses_in_progress += ['Python']

lecturer1 = Lecturer('Иван', 'Иванов')
lecturer1.courses_attached += ['Python']

lecturer2 = Lecturer('Анна', 'Смирнова')
lecturer2.courses_attached += ['Python']

reviewer = Reviewer('Пётр', 'Петров')
reviewer.courses_attached += ['Python']

# Оценки лекторам
student1.rate_lecture(lecturer1, 'Python', 9)
student1.rate_lecture(lecturer1, 'Python', 10)
student2.rate_lecture(lecturer2, 'Python', 7)

# Оценки студентам
reviewer.rate_hw(student1, 'Python', 8)
reviewer.rate_hw(student1, 'Python', 10)
reviewer.rate_hw(student2, 'Python', 6)

# Печать
print(student1)
print()
print(lecturer1)
print()
print(reviewer)
print()
print(f"Студент 1 лучше студента 2? {student1 > student2}")
print(f"Лектор 1 лучше лектора 2? {lecturer1 > lecturer2}")