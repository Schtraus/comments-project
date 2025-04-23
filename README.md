# 📝 Комментарии SPA (Vue + Django)

**SPA-приложение с функциональностью комментариев**, реализованное с использованием Django, Django REST Framework, WebSocket и Vue.js. Позволяет оставлять анонимные комментарии с капчей, вложениями и ответами.

---

## ⚙️ Функции

- ✅ Оставление комментариев без регистрации
- ✍️ Поля формы: Имя, Email, Домашняя страница, CAPTCHA, Текст, Файлы
- 🧵 Вложенные (каскадные) ответы на комментарии
- 🔁 Обновление новых комментариев в реальном времени (WebSocket)
- 📄 Поддержка изображений (JPG, PNG, GIF ≤ 320x240) и .txt файлов (≤ 100КБ)
- 🧼 Очистка HTML (bleach), разрешены: `<a>`, `<strong>`, `<i>`, `<code>`
- ⚙️ Сортировка: по имени, email и дате (ASC/DESC)
- 📑 Пагинация: 25 заглавных комментариев на страницу
- 🖼️ Предпросмотр текста до отправки

---

## 🛠 Стек технологий

- **Backend**: Django 5.2, DRF, Channels, Redis
- **Frontend**: Vue.js 3 (Vue CLI), Axios, Lightbox2
- **WebSocket**: Django Channels + Daphne
- **БД**: SQLite (или PostgreSQL/MySQL)
- **Контейнеризация**: Docker + Docker Compose
- **Хостинг**: AWS EC2

---

## 🚀 Запуск проекта локально

```bash
# Клонируем репозиторий
https://github.com/Schtraus/comments-project.git
cd comments-project

# Собираем и запускаем контейнеры
docker-compose up --build
```

Проект будет доступен по адресу:

- Локально: http://localhost:8080
- На сервере: http://13.60.5.138:8080

---


## 🗂 Структура проекта

```
comments-project/
├── backend/
│   ├── comments/
│   ├── config/
│   ├── media/
│   └── Dockerfile
├── frontend/
│   ├── src/
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 📷 Превью и схема БД

- 📽 Видео-демонстрация: *[https://youtu.be/eNYU10CVS44]*
- 📐 ER-схема: *models.png*

---
