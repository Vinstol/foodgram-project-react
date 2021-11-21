![Build Status](https://github.com/Vinstol/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?branch=master)

# Foodgram - «Продуктовый помощник», сервис с рецептами.
На этом сервисе авторизованные пользователи могут публиковать рецепты, подписываться на публикации других авторизованных пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
Неавторизованным пользователям доступна регистрация, авторизация, просмотр рецептов других авторов.

## Используемые технологии:
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

## Подготовка и запуск проекта:
### Склонировать репозиторий на локальную машину:
- git clone https://github.com/Vinstol/foodgram-project-react.git

## Для работы с удаленным сервером (на ubuntu):

### Выполните вход на свой удаленный сервер под своим именем пользователя (username). 
### Обновите список доступных к установке пакетов:
- sudo apt update

### Установите docker на сервер:
- sudo apt install docker.io 

### Установите docker-compose на сервер:
- sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

### Локально отредактируйте файл infra/nginx.conf: 
- в строке server_name впишите IP-адрес своего сервера (host).

### Скопируйте файлы docker-compose.yml и nginx.conf из директории infra на сервер:
- scp docker-compose.yml username@host:/home/username/docker-compose.yml
- scp nginx.conf username@host:/home/username/nginx.conf

### На сервере создайте файл backend.env и впишите в него следующие переменные окружения:
#### (Либо создайте файл backend.env локально и скопируйте на сервер аналогично предыдущему пункту)

- SECRET_KEY=  #сюда впишите секретный ключ проекта django.
- DB_ENGINE=django.db.backends.postgresql  # указываем, что работаем с postgresql.
- DB_NAME=  # имя базы данных.
- POSTGRES_USER=  # логин для подключения к базе данных.
- POSTGRES_PASSWORD=  # пароль для подключения к БД.
- DB_HOST=postgresql  # название сервиса (контейнера).
- DB_PORT=5432  # порт для подключения к БД.

### На сервере создайте файл postgresql.env для работы с контейнером postgres и впишите в него следующие переменные окружения:

- POSTGRES_DB=  # имя базы данных (должно совпадать с предыдущим пунктом).
- POSTGRES_USER=  # логин для подключения к базе данных (должно совпадать с предыдущим пунктом).
- POSTGRES_PASSWORD= # пароль для подключения к БД (должно совпадать с предыдущим пунктом).

### На сервере соберите docker-compose:
- sudo docker-compose up -d --build

### После успешной сборки контейнера подготовьте базу данных:
#### Вариант 1: Загрузка только ингредиентов:
- docker exec -it infra-backend-1 sh
- python manage.py loaddata fixtures/new_ingredients.json
- python manage.py createsuperuser
- exit

#### Вариант 2: Загрузка тестовой базы данных (с пользователями, рецептами и тегами):
- docker exec infra-backend-1 python manage.py loaddata fixtures/new_db.json

### В данный момент проект доступен по следующему адресу:
- https://vinstolbox.tk/
