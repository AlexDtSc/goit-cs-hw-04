##### ДЗ Тема 7. Основи багатопотокового програмування
##### ДЗ Тема 8. Основи багатопроцесорного програмування

# Частина 2. Реалізація багатопроцесорного підходу до обробки файлів (використовуючи multiprocessing) - Тема 8

'''
Технiчний опис завдання
Розробіть програму, яка паралельно обробляє та аналізує текстові файли для пошуку визначених ключових слів. Створіть дві версії програми: одну — з використанням модуля threading для багатопотокового програмування, та іншу — з використанням модуля multiprocessing для багатопроцесорного програмування.

Покрокова інструкція

1. Реалізація багатопотокового підходу до обробки файлів (використовуючи threading):

Розділіть список файлів між різними потоками.
Кожен потік має шукати задані ключові слова у своєму наборі файлів.
Зберіть і виведіть результати пошуку з усіх потоків.


2. Реалізація багатопроцесорного підходу до обробки файлів (використовуючи multiprocessing):

Розділіть список файлів між різними процесами.
Кожен процес має обробляти свою частину файлів, шукаючи ключові слова.
Використайте механізм обміну даними (наприклад, через Queue) для збору та виведення результатів пошуку.


Критерії прийняття
- Реалізовано багатопотоковий та багатопроцесорний підходи до обробки файлів.
- Забезпечено розподілення файлів між потоками/процесами.
- Код вимірює та виводить час виконання для кожної з версій.
- Забезпечено обробку помилок і винятків, особливо при роботі з файловою системою.
- Обидві версії програми повертають словник, де ключ — це пошукове слово, а значення — список шляхів файлів, де це слово знайдено.
'''

# exercise_7_multiprocessing.py
import multiprocessing
import timeit
from collections import defaultdict
from pathlib import Path


def search_in_file(file_path, keywords):
    found = defaultdict(list)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    found[keyword].append(file_path)
    except Exception as e:
        print(f"Помилка при читанні {file_path}: {e}")
    return found


def merge_dicts(dict_list):
    merged = defaultdict(list)
    for d in dict_list:
        for k, v in d.items():
            merged[k].extend(v)
    return merged


def main_multiprocessing(file_paths, keywords):
    if not file_paths:
        print("Немає файлів для обробки. Переконайтесь, що папка 'input' існує і містить .py файли.")
        return {}    

    start = timeit.default_timer()

    with multiprocessing.Pool(processes=4) as pool:
        results = pool.starmap(search_in_file, [(file_path, keywords) for file_path in file_paths])

    combined_results = merge_dicts(results)

    end = timeit.default_timer()
    print(f"\nЧас виконання з multiprocessing: {end - start:.4f} секунд\n")
    return combined_results


if __name__ == '__main__':
    file_paths = list(Path("input").glob("*.py"))
    print(f"Обробляємо файли: {file_paths}\n")

    keywords = ["print", "def", "import"]
    results = main_multiprocessing(file_paths, keywords)

    print("Результати пошуку:", dict(results))
