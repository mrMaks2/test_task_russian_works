# Обработчик банковских Webhook-ов


Эта внутренняя служба на базе Django предназначена для обработки входящих Webhook-ов из банка, обработки платежей и обновления балансов организации.

## Функции

- **Обработка Webhook-ов**
- **Защита от дублирования**
- **Обновления баланса**
- **Логирование**

## Используемые инструменты

- Python
- Django
- Django REST Framework
- MySQL

## Эндпоинты

- `POST /api/webhook/bank/`: Принимает webhook для дальнейшей обработки.
- `GET /api/organizations/<inn>/balance/`: Возвращает текущий баланс организации.


## Инструкции по настройке

1.  **Клонировать репозиторий.**
2.  **Создайте виртуальное окружение:** `python -m venv venv`
3.  **Активируйте виртуальное окружение:**
    -   Для Windows: `venv\Scripts\activate`
    -   Для macOS и Linux: `source venv/bin/activate`
4.  **Установить зависимости:** `pip install -r requirements.txt`
5.  **Настроить базу данных:** Обновите настройки `DATABASES` в `backend/bank_webhook/settings.py` с вашими учетными данными БД MySQL.
6.  **Создайте и примите миграции:** `python manage.py makemigrations && python manage.py migrate`
7.  **Создайте суперюзера (при необходимости):** `python manage.py createsuperuser`