##### ДЗ Тема 7. Основи багатопотокового програмування
##### ДЗ Тема 8. Основи багатопроцесорного програмування

# Частина 1. Реалізація багатопотокового підходу до обробки файлів (використовуючи threading) - Тема 7

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

# exercise_7_threading.py
import threading
import timeit
from collections import defaultdict
from pathlib import Path


def search_in_file(file_path, keywords, results, lock):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    with lock:  # Забезпечення безпеки потоків
                        results[keyword].append(file_path)
    except Exception as e:
        print(f"Помилка при читанні {file_path}: {e}")


def thread_task(files, keywords, results, lock):
    for file in files:
        search_in_file(file, keywords, results, lock)


def main_threading(file_paths, keywords):
    if not file_paths:
        print("Немає файлів для обробки. Переконайтесь, що папка 'input' існує і містить .py файли.")
        return {}
    
    start = timeit.default_timer()

    num_threads = 4
    threads = []
    results = defaultdict(list)
    lock = threading.Lock()

    # Ефективний поділ файлів між потоками
    chunk_size = (len(file_paths) + num_threads - 1) // num_threads
    file_chunks = [file_paths[i:i + chunk_size] for i in range(0, len(file_paths), chunk_size)]

    for i in range(num_threads):
        thread = threading.Thread(target=thread_task, args=(file_chunks[i], keywords, results, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end = timeit.default_timer()
    print(f"\nЧас виконання з threading: {end - start:.4f} секунд\n")
    return results


if __name__ == '__main__':
    file_paths = list(Path("input").glob("*.py"))
    print(f"Обробляємо файли: {file_paths}\n")

    keywords = ["print", "def", "import"]
    results = main_threading(file_paths, keywords)

    print("Результати пошуку:", dict(results))

