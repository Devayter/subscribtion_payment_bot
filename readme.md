# Стек технологий в проекте

* Aiogram
* Python
* SQLite

## Описание проекта

Проект SubscribtionPaymentBot - это бот для оплаты подписки в Telegram. Его функциональность включает прием платежей, выдачу ссылок, уведомление о сроках подписки, управление заявками в группе и оповещение пользователей о скором окончании подписки, а также удаление их из группы после истечения срока подписки.

<img width="534" alt="image" src="https://github.com/Devayter/subscribtion_payment_bot/assets/103175986/2f0f69f3-a4b7-4113-ab9d-cf14a2be9d9b">


## Подготовка проекта

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone git@github.com:Devayter/subscribtion_payment_bot.git
```

```bash
cd subscribtion_payment_bot
```

Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```bash
    source venv/bin/activate
    ```

* Если у вас windows

    ```bash
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt

```bash
python3 -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

### Для настройки проекта необходимо указать следующие переменные окружения в файле ".env"

* Токен бота Telegram
* ID группы в Telegram
* DATABASE_URL
* Токен оплаты

### Запуск бота

```bash
python3 app/main.py
```

## Ссылка на бота

[SubscribtionPaymentBot](https://t.me/jutsabot)

## Авторы

* [Павел Рябов](https://github.com/Devayter/)
