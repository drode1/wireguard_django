# Wireguard VPN

Проект помогает управлять соединениями Wireguard. Можно создавать новые конфиги и пиры (клиентские соединения) и они
будут автоматически привязываться к нужному конфигу.
Проект позволяет добавлять неограниченное количество пользователей, а настроить конфигурацию можно
с помощью файла или через Telegram бот.

**TODO** проекта описан ниже.

## Стек

![python version](https://img.shields.io/badge/Python-3.11-green)
![django version](https://img.shields.io/badge/Django-4.1-green)
![djangorestframework version](https://img.shields.io/badge/DRF-3.14-green)
![djangorestframeworksimplejwt version](https://img.shields.io/badge/DRF_simplejwt-5.2.2-green)

## Что внутри?

1. User – приложение для управления пользователями;
2. Wireguard – приложение для управления конфигами, интерфейсами WG;
3. Core – приложение для хранения базовых моделей;
4. API – приложение для работы с API;
5. Service – приложение для хранения и создания вспомогательных функций;

### Как запустить проект локально с помощью venv:

1. Клонировать репозиторий и перейти в него в командной строке:

    ```
    cd wireguard_django
    ```

2. Cоздать и активировать виртуальное окружение:

    ```
    python3.11 -m venv venv
    . venv/bin/activate
    python -m pip install --upgrade pip
    ```    

3. Установить зависимости из файла requirements.txt:

    ``` 
    pip install -r requirements.txt
    ```   

4. Выполнить миграции:

    ```
    python manage.py migrate
    ```       

5. Запустить проект:

    ```
    python manage.py runserver
    ```

---

## TODO List:

1. Добавить Docker
2. Покрыть тестами основные компоненты;
3. При добавлении новой порции пользователей запускать wg-quick скрипт для обновления конфига;
4. Добавить отслеживания трафика и подключений через wg show;
5. Добавить мультиязычность проекта;
6. Добавить workflow для деплоя;

---

## Контакты

- Егор Ремезов
    - [GitHub](https://github.com/drode1)
    - [Telegram](https://t.me/e_remezov)
    - [Mail](mailto:info@eremezov.com)