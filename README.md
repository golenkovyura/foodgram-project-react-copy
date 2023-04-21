
![Здесь видно, что workflow прошел успешно](https://github.com/yanastasya/foodgram-project-react/actions/workflows/main.yml/badge.svg)
### Стек технологий:
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)


### Приложение «Продуктовый помощник»: 
Сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать и скачивать список продуктов, которые нужно купить для приготовления выбранных блюд.

В данный момент прект запущен на сервере Yandex.Cloud и доступен [здесь](http://158.160.59.159/recipes/)

[Докуметация к API](http://158.160.59.159/api/docs/)

[Админка](http://158.160.59.159/admin/) (email: admin@mail.ru password:qwerty)

Проект упакован в контейнеры и настроены следующие процессы: запуск тестов, обнавление образа проекта на DockerHub, автоматический деплой на боевой сервер при пуше в главную ветку master.

### Для разворота проекта локально:
1) Установить и запустить [![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
2) Скачать данный репозиторий
3) В директории infra создать файл env. и наполнить его по образцу ниже:
  -  DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
  -  DB_NAME=postgres # имя базы данных
  -  POSTGRES_USER=postgres # логин для подключения к базе данных
  -  POSTGRES_PASSWORD=qwerty # пароль для подключения к БД (установите свой)
  -  DB_HOST=db # название сервиса (контейнера)
  -  DB_PORT=5432 # порт для подключения к БД
4) из директории infra/ выполнить команду 
``` docker-compose up -d --build ```
5) после того как контейнеры nginx, db (БД PostgreSQL) и backend будут запущены, выполнить команды:
 ```
    sudo docker-compose exec web backend
    python manage.py migrate
    python manage.py collectstatic --no-input
    python manage.py createsuperuser
    python manage.py load_ingredienta_data
    python manage.py load_tags_data
 ```

6) Теперь прект доступен по адресам:
[главная страница](http://localhost/recipes/)
[Докуметация к API](http://localhost/api/docs/)
[Админка](http://localhost/admin/)


### Для разворота проекта на удалённом сервере:
1) форкнуть данный репозитарий
2) в директориях backend и frontend находятся файлы Dockerfile. Необходимо собрать эти 2 образа и сохранить их на вашем репозитории DockerHub под соответствующими именами.
3) подготовьте сервер к деплою: необходимо установить docker, docker-compose
4) в файлах docker-compose.yaml (строка 14) и yamdb_workflow.yml (строки 55 и  72) изменить "yanastasya" на ваш username на DockerHub. 
5) скопировать файлы docker-compose.yaml и nginx.conf и папку docs/ из проекта на сервер в домашнюю директорию
6) Добавьте в Secrets GitHub Actions переменные окружения для работы базы данных:
  -  DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
  -  DB_NAME=postgres # имя базы данных
  -  POSTGRES_USER=postgres # логин для подключения к базе данных
  -  POSTGRES_PASSWORD=qwerty # пароль для подключения к БД (установите свой)
  -  DB_HOST=db # название сервиса (контейнера)
  -  DB_PORT=5432 # порт для подключения к БД
  -  HOST=внешний IP сервера
  -  USER=имя пользователя для подключения к серверу
  -  SSH_KEY=приватный ключ с компьютера, имеющего доступ к боевому серверу
  -  PASSPHRASE=фраза-пароль ,если использовали её при создании ssh-ключа  
  -  DOCKER_USERNAME и DOCKER_PASSWORD - ваши логин и пароль на докерхаб.
    
6) выполните git push в ветку master, после чего будет запущен workflow: проверка кода flake8, обновление образов backend и frontend на вашем репозитории DockerHub и деплой на сервер
7) после успешного деплоя зайти на сервер и выполнить команды:
    ```
    sudo docker-compose exec backend bash
    python manage.py migrate
    python manage.py collectstatic
    python manage.py createsuperuser
    python manage.py load_ingredienta_data
    python manage.py load_tags_data
    ```
6) Теперь прект доступен по адресам:

- Главная страница: http://<внешний IP сервера>/recipes/
- Докуметация к API: http://<внешний IP сервера>/api/docs/
- Админка: http://<внешний IP сервера>/admin/

### Авторы:
backend - [Я](https://github.com/yanastasya)
frontend - Яндекс.Практикум
