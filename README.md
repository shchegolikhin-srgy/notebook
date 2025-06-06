# 📋 To-Do list

Веб-приложение "Список задач", позволяющее добавлять, удалять, изменять и завершать задачи.  
Приложение поддерживает регистрацию и авторизацию пользователей через базу данных.

---

## 🧩 Функционал

- ✅ Регистрация и вход через форму
- ✅ Добавление новых задач
- ✅ Удаление задач
- ✅ Изменение текста задачи
- ✅ Отметка о выполнении задачи
- ✅ Все данные привязаны к пользователю

---

## 🛠 Технологии

- python 3.12+
- fastapi
- jinja2 
- asyncpg 
- uvicorn
- docker 
- slowapi
- argon2-cffi
- python-jose
- pyjwt
---

## 🚀 Как запустить локально

### 1. Клонируй репозиторий:

```bash
git clone https://github.com/shchegolikhin-srgy/todo-list.git
cd todo-list
```

### 2. Создай виртуальное окружение:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# Или на Windows:
# .venv\Scripts\activate
```

### 3. Установи зависимости:

```bash
pip install -r app/requirements.txt
```

### 4. Настрой базу данных

Создай PostgreSQL базу данных и обнови `DATABASE_URL` в `.env` файле:

```env
DATABASE_URL=postgresql://user:password@localhost/your_db
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> Убедись, что таблицы созданы. Пример миграции:
```sql
CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    hashed_password TEXT NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user'
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,          
    text VARCHAR(255) NOT NULL,    
    user_id INTEGER NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    completed BOOLEAN
);
```

### 5. Запусти сервер:

```bash
uvicorn app.main:app --reload 
```

Открой в браузере:
🔗 [http://127.0.0.1:8000/home](http://127.0.0.1:8000/home)

Страница входа:  
🔗 [http://127.0.0.1:8000/login](http://127.0.0.1:8000/login)

---

## 🐳 Как запустить через Docker

### 1. Собери образ:

```bash
docker build -t todo-list .
```

### 2. Запусти контейнер:

```bash
docker run -p 8000:8080 -d todo-list
```

Открой в браузере:  
🔗 [http://127.0.0.1:8000/home](http://127.0.0.1:8000/home)

---

## 🔒 Безопасность

- Пароли хэшируются через `argon2`
- Защита от SQL-иньюкций
- Ограничение попыток входа в аккаунт до 3 раз в минуту
- JWT токены используются для аутентификации
- Все действия доступны только авторизованным пользователям

---

## 📦 В будущем можно добавить

- Админ панель
- REST API для мобильных клиентов
- Фильтры и категории задач
- Email подтверждение регистрации
- Поддержку Redis и кэширования

---

## 💬 Обратная связь

Если у тебя есть вопросы или предложения — пиши в Issues или свяжись напрямую!

---

## ❤️ Спасибо за использование!
