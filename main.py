import json
import os
import sys

STUDENTS_FILE = "students.json"

users = {
    "admin": {"password": "admin123", "role": "admin"},
    "student1": {"password": "student1", "role": "user"},
}

students = [
    {"id": 1, "name": "Майя Шевченко", "age": 17, "class": "11", "grade": "4"},
    {"id": 2, "name": "Александра Степанова", "age": 18, "class": "11", "grade": "4"},
    {"id": 3, "name": "Дарина Мирокина", "age": 16, "class": "10", "grade": "5"},
]

# Авторизация
def authenticate():
    print("Авторизация\n")
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    if username in users and users[username]["password"] == password:
        print(f"Добро пожаловать, {username}!")
        return username
    else:
        print("Неверное имя пользователя или пароль. Попробуйте снова.")
        return None

# Проверка роли пользователя
def check_role(username):
    return users[username]["role"]


def load_students():
    if os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []  # Возвращаем пустой список, если файл не найден

# Сохранение списка учеников в файл JSON
def save_students(students):
    with open(STUDENTS_FILE, 'w', encoding='utf-8') as file:
        json.dump(students, file, ensure_ascii=False, indent=4)

# Просмотр списка учеников
def view_students():
    print("\nСписок учеников:")
    for student in students:
        print(f"{student['id']}. {student['name']}, Возраст: {student['age']}, Класс: {student['class']}, Оценка: {student['grade']}")

# Добавление ученика
def add_student():
    name = input("Введите имя ученика: ")
    age = int(input("Введите возраст ученика: "))
    st_class = input("Введите класс ученика: ")
    grade = input("Введите оценку ученика: ")
    new_id = len(students) + 1
    students.append({"id": new_id, "name": name, "age": age, "class": st_class, "grade": grade})
    print(f"Ученик {name} добавлен!")

# Удаление ученика
def delete_student():
    student_id = int(input("Введите ID ученика для удаления: "))
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        students.remove(student)
        print(f"Ученик {student['name']} удален!")
    else:
        print("Ученик с таким ID не найден.")

# Фильтрация и сортировка
def filter_and_sort_students():
    print("\nФильтрация учеников:")
    filter_type = input("Фильтровать по возрасту (1) или по оценке (2)? (Введите 1 или 2): ")
    if filter_type == '1':
        age_filter = int(input("Введите минимальный возраст: "))
        filtered_students = filter(lambda x: x['age'] >= age_filter, students)
    elif filter_type == '2':
        grade_filter = input("Введите минимальную оценку (5, 4, 3, 2, 0): ").upper()
        filtered_students = filter(lambda x: x['grade'] <= grade_filter, students)
    else:
        print("Неверный выбор фильтра.")
        return

    sorted_students = sorted(filtered_students, key=lambda x: x['age'])  # Сортировка по возрасту
    print("\nОтфильтрованные и отсортированные ученики:")
    for student in sorted_students:
        print(f"{student['id']}. {student['name']}, Возраст: {student['age']}, Оценка: {student['grade']}")

# Главная функция для меню
def main():
    valid = True
    while valid:
        username = authenticate()
        if username is None:
            continue

        role = check_role(username)
        while True:
            print("\nГлавное меню:")
            print("1. Просмотр списка учеников")
            if role == "admin":
                print("2. Добавить ученика")
                print("3. Удалить ученика")
                print("4. Фильтрация и сортировка учеников")
            print("5. Выйти")

            choice = input("Выберите действие: ")

            if choice == "1":
                view_students()
            elif choice == "2" and role == "admin":
                add_student()
            elif choice == "3" and role == "admin":
                delete_student()
            elif choice == "4" and role == "admin":
                filter_and_sort_students()
            elif choice == "5":
                save_students(students)
                print("Выход из программы...")
                valid = False
                sys.exit()
            else:
                print("Неверный выбор, попробуйте снова.")

# Запуск программы
if __name__ == "__main__":
    main()
