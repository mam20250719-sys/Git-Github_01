# Шаг 1. Создание репозитория (выполняется после ручного создания репозитория на GitHub)
git clone https://github.com/ваш-аккаунт/book-tracker.git
cd book-tracker

# Шаг 2. Создание начальных файлов

# .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
venv/
env/
.vscode/
.idea/
EOF

# books.json
cat > books.json << 'EOF'
[]
EOF

# README.md (начальный)
cat > README.md << 'EOF'
# Трекер прочитанных книг

Консольное приложение для учёта прочитанных книг.

## Как запустить
\`\`\`bash
python main.py
\`\`\`
EOF

# Фиксация первого коммита
git add README.md .gitignore books.json
git commit -m "feat: инициализация проекта — README, .gitignore, пустой books.json"
git push origin main

# Шаг 3. Создание веток
git checkout -b feature/add-book
git checkout main
git checkout -b feature/list-and-stats
git checkout main
git checkout -b feature/delete
git checkout feature/add-book  # переходим в первую ветку

# Шаг 4. Создание каркаса приложения main.py
cat > main.py << 'EOF'
import json
import os
from datetime import datetime

BOOKS_FILE = 'books.json'

def load_books():
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_books(books):
    with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

def add_book():
    pass

def list_books():
    pass

def show_average_rating():
    pass

def author_stats():
    pass

def delete_book():
    pass

def main():
    while True:
        print("\\n1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Показать среднюю оценку")
        print("4. Статистика по авторам")
        print("5. Удалить книгу")
        print("6. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            list_books()
        elif choice == '3':
            show_average_rating()
        elif choice == '4':
            author_stats()
        elif choice == '5':
            delete_book()
        elif choice == '6':
            break
        else:
            print("Неверный выбор!")

if __name__ == "__main__":
    main()
EOF

git add main.py
git commit -m "feat: базовый каркас приложения с меню"

# Шаг 5. Реализация feature/add-book
cat >> main.py << 'EOF'

def add_book():
    books = load_books()
    title = input("Название книги: ")
    author = input("Автор: ")

    # Проверка на дубликат
    if any(book['title'] == title and book['author'] == author for book in books):
        print("Эта книга уже есть в списке!")
        return

    while True:
        try:
            rating = int(input("Оценка (1–5): "))
            if 1 <= rating <= 5:
                break
            else:
                print("Оценка должна быть от 1 до 5.")
        except ValueError:
            print("Введите число!")

    date = datetime.now().strftime("%Y-%m-%d")

    new_book = {
        'title': title,
        'author': author,
        'rating': rating,
        'date': date
    }
    books.append(new_book)
    save_books(books)
    print(f"Книга '{title}' добавлена!")
EOF

git add main.py
git commit -m "feat(add-book): реализация добавления книги с валидацией оценки и проверкой дубликатов"
git push origin feature/add-book

# Шаг 6. Реализация feature/list-and-stats
git checkout main
git pull origin main
git checkout -b feature/list-and-stats

cat >> main.py << 'EOF'

def list_books():
    books = load_books()
    if not books:
        print("Книг нет.")
        return
    print("\\nСписок книг:")
    for i, book in enumerate(books, 1):
        print(f"{i}. {book['title']} — {book['author']} (оценка: {book['rating']}, дата: {book['date']})")

def show_average_rating():
    books = load_books()
    if not books:
        print("Книг нет для расчёта.")
        return
    avg = sum(book['rating'] for book in books) / len(books)
    print(f"\\nСредняя оценка: {avg:.2f}")

def author_stats():
    books = load_books()
    if not books:
        print("Книг нет для статистики.")
        return
    stats = {}
    for book in books:
        author = book['author']
        stats[author] = stats.get(author, 0) + 1
    print("\\nСтатистика по авторам:")
    for author, count in stats.items():
        print(f"{author}: {count} книг")
EOF

git add main.py
git commit -m "feat(list-stats): вывод списка книг, средней оценки и статистики по авторам"
git push origin feature/list-and-stats

# Шаг 7. Реализация feature/delete
git checkout main
git pull
git checkout -b feature/delete

cat >> main.py << 'EOF'

def delete_book():
    books = load_books()
    list_books()
    try:
        index = int(input("Введите номер книги для удаления: ")) - 1
        if 0 <= index < len(books):
            removed = books.pop(index)
            save_books(books)
            print(f"Книга '{removed['title']}' удалена.")
        else:
            print("Неверный номер!")
    except ValueError:
        print("Введите число!")
EOF

git add main.py
git commit -m "feat(delete): реализация удаления книги по номеру"
git push origin feature/delete

# Шаг 8. Слияние веток (минимум один PR через GitHub)
git checkout main
git merge feature/list-and-stats
git merge feature/delete
git push

# Шаг 9. Обновление README.md
git checkout main
cat > README.md << 'EOF'
# Трекер прочитанных книг

Консольное приложение для учёта прочитанных книг с меню и сохранением в JSON.

## Функционал
* Добавление книги (с проверкой дубликатов и валидацией оценки)
* Вывод списка всех книг
* Расчёт средней оценки
* Статистика по авторам
* Удаление книги по номеру

## Как запустить
\`\`\`bash
python main.py
\`\`\`

## Пример работы
1. Добавить книгу
2. Показать все книги
3. Показать среднюю оценку
4. Статистика по авторам
5. Удалить книгу
6. Выход
Выберите действие: 1
Название книги: 1984
Автор: Джордж Оруэлл
Оценка (1–5): 5
Книга '1984' добавлена!
EOF

git add README.md
git commit -m "docs: обновление README с описанием функционала и примером работы"
git push origin main
