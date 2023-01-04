# Wireguard VPN

Приложение позволяет управлять VPN конфигами, с помощью админ панели и API

## Стек

![python version](https://img.shields.io/badge/Python-3.11-green)
![django version](https://img.shields.io/badge/Django-4.1-green)

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