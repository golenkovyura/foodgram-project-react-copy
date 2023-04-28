Дипломный проект курса Backend python-разработчик от Яндекс.Практикум, который я проходила с 06.2022 по 04.2023.

Есть 4 варианта, как увидеть результат моей работы (что скрывается за кодом в этом репозитории?):
- Сообщите мне о своем желании [ВК](https://vk.com/nastya_klincova) или Telegram @AnastasyaKlincova. Я запущу виртуальную машину на сервере и дам вам ссылку.
- Если на вашем ПК установлен Python3: скачайте репозиторий и следуйте инструкциям в README.
- Если на вашем ПК установлен Python3 и Docker, вы можете развернуть проект в контейнерах и запустить локально. Инструкции здесь.
- Если у вас есть доступ к удалённому серверу и вы не против установить не него Docker и Docker-compose, то здесь описано, как поднять проект на боевом сервере.
        
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![djoser](https://img.shields.io/badge/-djoser-464646?style=flat-square)](https://djoser.readthedocs.io/en/latest/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

Задание состояло в следующем:
- написать бекэенд (API) к онлайн-сервису "Продуктовый помощник" по техническому заданию (спецификация API). 
- подключить к приложению СУБД PostgreSQL
- "подружить" бекэнд c фронтендом. (фронт был дан в виде приложения React)
- Запустить проект на сервере в Яндекс.Облаке в трёх контейнерах: nginx, PostgreSQL и Django+Gunicorn. Контейнер с проектом должен обновляется на Docker Hub.
В nginx настроена раздача статики, остальные запросы переадресуются в Gunicorn. Данные сохраняются в volumes.

Работа была принята по итогам трёх код-ревью с комментариями по улучшению кода.

Далее более подробно о сервисе Продуктовый помощник, инструкции по развороту проекта локально и на сервере. А также пример работы API на одном из эндпоинтов с комментариями по реализации. 

## Оглавление

0. [сайт Foodgram, «Продуктовый помощник». Техническое описание проекта](#Сайт Foodgram, «Продуктовый помощник». Техническое описание проекта)
1. [Инструкции по развороту проекта](#Инструкции по развороту проекта)
2. [Примеры запросов и ответов к API](#Примеры запросов и ответов к API)
3. [Текст ссылки](#твоё_название)
    
## Сайт Foodgram, «Продуктовый помощник». Техническое описание проекта

<a name="твоё_название">Сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать и скачивать список продуктов, которые нужно купить для приготовления выбранных блюд.</a>


### Сервисы и страницы проекта

### Главная страница
Содержимое главной страницы — список первых шести рецептов, отсортированных по дате публикации (от новых к старым).  Остальные рецепты доступны на следующих страницах: внизу страницы есть пагинация.

### Страница рецепта
На странице — полное описание рецепта. Для авторизованных пользователей — возможность добавить рецепт в избранное и в список покупок, возможность подписаться на автора рецепта.

### Страница пользователя
На странице — имя пользователя, все рецепты, опубликованные пользователем и возможность подписаться на пользователя.

### Подписка на авторов
Подписка на публикации доступна только авторизованному пользователю. Страница подписок доступна только владельцу.

Сценарий поведения пользователя:
1. Пользователь переходит на страницу другого пользователя или на страницу рецепта и подписывается на публикации автора кликом по кнопке «Подписаться на автора».
2. Пользователь переходит на страницу «Мои подписки» и просматривает список рецептов, опубликованных теми авторами, на которых он подписался. Сортировка записей — по дате публикации (от новых к старым)
3. При необходимости пользователь может отказаться от подписки на автора: переходит на страницу автора или на страницу его рецепта и нажимает «Отписаться от автора».

### Список избранного
Работа со списком избранного доступна только авторизованному пользователю. Список избранного может просматривать только его владелец.

Сценарий поведения пользователя:
1. Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в избранное».
2. Пользователь переходит на страницу «Список избранного» и просматривает персональный список избранных рецептов.
3. При необходимости пользователь может удалить рецепт из избранного.

### Список покупок
Работа со списком покупок доступна авторизованным пользователям. Список покупок может просматривать только его владелец.

Сценарий поведения пользователя:

1. Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в покупки».
2. Пользователь переходит на страницу Список покупок, там доступны все добавленные в список рецепты. Пользователь нажимает кнопку Скачать список и получает файл с суммированным перечнем и количеством необходимых ингредиентов для всех рецептов, сохранённых в «Списке покупок».
3. При необходимости пользователь может удалить рецепт из списка покупок.
Список покупок скачивается в формате .txt (или, по желанию, можно сделать выгрузку PDF).

При скачивании списка покупок ингредиенты в результирующем списке не должны дублироваться; если в двух рецептах есть сахар (в одном рецепте 5 г, в другом — 10 г), то в списке должен быть один пункт: Сахар — 15 г.

В результате список покупок может выглядеть так:
> Фарш (баранина и говядина) (г) — 600
> Сыр плавленый (г) — 200
> Лук репчатый (г) — 50
> Картофель (г) — 1000


### Фильтрация по тегам
При нажатии на название тега выводится список рецептов, отмеченных этим тегом. Фильтрация может проводится по нескольким тегам в комбинации «или»: если выбраны несколько тегов — в результате должны быть показаны рецепты, которые отмечены хотя бы одним из этих тегов. 
При фильтрации на странице пользователя должны фильтроваться только рецепты выбранного пользователя. Такой же принцип должен соблюдаться при фильтрации списка избранного.

### Регистрация и авторизация
В проекте должна быть доступна система регистрации и авторизации пользователей. Чтобы собрать весь код для управления пользователями воедино — создайте приложение users. 

#### Обязательные поля для пользователя:
- Логин
- Пароль
- Email
- Имя
- Фамилия

#### Уровни доступа пользователей:
- Гость (неавторизованный пользователь)
- Авторизованный пользователь
- Администратор

#### Что могут делать неавторизованные пользователи
- Создать аккаунт.
- Просматривать рецепты на главной.
- Просматривать отдельные страницы рецептов.
- Просматривать страницы пользователей.
- Фильтровать рецепты по тегам.

#### Что могут делать авторизованные пользователи
- Входить в систему под своим логином и паролем.
- Выходить из системы (разлогиниваться).
- Менять свой пароль.
- Создавать/редактировать/удалять собственные рецепты
- Просматривать рецепты на главной.
- Просматривать страницы пользователей.
- Просматривать отдельные страницы рецептов.
- Фильтровать рецепты по тегам.
- Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов.
- Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл с количеством необходимых ингридиентов для рецептов из списка покупок.
- Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.

#### Что может делать администратор
Администратор обладает всеми правами авторизованного пользователя. 
Плюс к этому он может:
- изменять пароль любого пользователя,
- создавать/блокировать/удалять аккаунты пользователей,
- редактировать/удалять любые рецепты,
- добавлять/удалять/редактировать ингредиенты.
- добавлять/удалять/редактировать теги.
- Все эти функции нужно реализовать в стандартной админ-панели Django.

### Технические требования и инфраструктура
- Проект должен использовать базу данных PostgreSQL.
- Код должен находиться в репозитории foodgram-project-react.
- В Django-проекте должен быть файл requirements.txt со всеми зависимостями.
- Проект нужно запустить в трёх контейнерах (nginx, PostgreSQL и Django) (контейнер frontend используется лишь для подготовки файлов) через docker-compose на вашем сервере в Яндекс.Облаке. Образ с проектом должен быть запушен на Docker Hub.
____
[:arrow_up:Оглавление](#Оглавление)
___

## Инструкции по развороту проекта

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
5) после того как контейнеры nginx, db (БД PostgreSQL) и backend будут запущены, необходимо в контейнере backend создать и применить миграции, собрать статику, создать суперпользователя и загрузить данные с ингредиентами и тегами для создания рецептов. Для этого последовательно выполнить следующие команды:
 ```
    (sudo)* docker-compose exec web backend
    python manage.py makemigrations users
    python manage.py makemigrations recipes
    python manage.py migrate
    python manage.py collectstatic --no-input
    python manage.py createsuperuser
    python manage.py load_ingredienta_data
    python manage.py load_tags_data
 ```
 * - если ОС Linux

6) Теперь проект доступен по адресам:
[главная страница](http://localhost/recipes/)

[Докуметация к API](http://localhost/api/docs/)

[Админка](http://localhost/admin/)


### Для разворота проекта на удалённом сервере:
1) форкнуть данный репозитарий
2) в директориях backend и frontend находятся файлы Dockerfile. Необходимо собрать эти 2 образа и сохранить их на вашем репозитории DockerHub под соответствующими именами.
3) подготовьте сервер к деплою: необходимо установить docker, docker-compose
4) в файлах docker-compose.yaml (строка 14) и yamdb_workflow.yml (строки 55 и  72) изменить "yanastasya" на ваш username на DockerHub. 
5) в файле nginx.conf изменить server name на внешний io вашего сервера.
6) скопировать файлы docker-compose.yaml и nginx.conf и папку docs/ из проекта на сервер в домашнюю директорию
7) Добавьте в Secrets GitHub Actions переменные окружения для работы базы данных:
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
    
6) выполните git push в ветку master, после чего будет запущен workflow: проверка кода flake8, обновление образа backend на вашем репозитории DockerHub и деплой на сервер
7) после успешного деплоя зайти на сервер и выполнить команды:
    ```
    (sudo)* docker-compose exec web backend
    python manage.py makemigrations users
    python manage.py makemigrations recipes
    python manage.py migrate
    python manage.py collectstatic --no-input
    python manage.py createsuperuser
    python manage.py load_ingredienta_data
    python manage.py load_tags_data
    ```
    * - если ОС Linux
6) Теперь прект доступен по адресам:

- Главная страница: http://<внешний IP сервера>/recipes/
- Докуметация к API: http://<внешний IP сервера>/api/docs/
- Админка: http://<внешний IP сервера>/admin/

## Примеры запросов и ответов к API.

Ниже опишу требования из ТЗ к работе эндпоинта api/recipes/{id} и прокомментирую то, как это было реализованно.
Более подробно о других эндпоинтах можете увидеть в документации. Она будет доступна к просмотру после разворота проекта. Инструкции для этого смотри в гл.1
Код, реализующий работу API, смотри в директории [backend](https://github.com/yanastasya/foodgram-project-react/tree/master/backend) 

### ``` /api/recipes/{id}```
#### GET запрос: просмотр списка всех рецептов или отдельного рецепта по id.

> В urls.py данный маршрут задан с помощью DefaultRouter 
> Код смотри здесь [urls.py](https://github.com/yanastasya/foodgram-project-react/blob/master/backend/api/urls.py)
> Эндпоинт обрабатывается контроллером RecipeViewSet

Доступно всем пользователям.
> В конфиге проекта установлены дефолтные права доступа только для авторизованных пользовтелей. Во вьюсете RecipeViewSet установлен кастомный пермишн IsAuthorOrAdminOrReadOnly, дающий право просмотра рецептов любому поьзователю, создания рецептов любому авторизованному пользователю, а право на редактирование и удаление рецепта только админу и автору данного рецепта.
> Код смотри здесь [permissions.py](https://github.com/yanastasya/foodgram-project-react/blob/master/backend/api/permissions.py)

В запрос могут быть добавлены параметры для пагинации и фильтрации:

- page - номер страницы

- limit - колличество объектов на странице

> Использован кастомный класс для пагинации, дочерний от встроеного PageNumberPagination. Переопределён параметр page_size_query_param
> Код смотри здесь [pagination.py](https://github.com/yanastasya/foodgram-project-react/blob/master/backend/api/pagination.py)

- author - вернуть только рецепты автора с заданным id

- tags - вернуть только рецепты, отмеченные тагами (по slug), возможно перечисление через &

- is_favorite - вернуть только рецепты ,добавленные в список избранного пользователем, делающим запрос

- is_in_shopping_cart - вернуть только рецепты ,добавленные в список покупок пользователем, делающим запрос

> Использован кастомный фильтр. Признаюсь, это далось мне тяжело. Было перепробовано много вариантов, хотела сделать более компактно. Это решение мне подсказали, оно хоть и громоздкое, но явное, взяла его себе.
> Код смотри здесь [filters.py](https://github.com/yanastasya/foodgram-project-react/blob/master/backend/api/filters.py)

Пример ответа:
```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```
> Для обработки запросов на просмотр и создание рецепта используются разные сериализаторы. В RecipeGetSerializer (для просмотра) поля tags, author и ingradients возвращаются в виде объекта. Пришлось немного пострадать, чтобы добиться того, чтобы ingredient возвращался с id, name, measure_unit объекта модели Ingredient, а amount из объекта модели, связывающей рецепт с ингредиентом (IngredientInRecipe). Здесь оказалось, что я не совсем понимаю, как работают сериализаторы в джанго, пришлось разбираться.
> Поля is_favorited и is_in_shopping_cart определены отдельными методами.
> Код смотри здесь [serializers.py](https://github.com/yanastasya/foodgram-project-react/blob/master/backend/api/serializers.py)


###  ``` /api/recipes/```
#### POST запрос: создание рецепта.
Доступно только авторизованному пользователю.
Пример запроса(все поля обызательны):

```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```
> Все поля обязательны. Название рецепта не должно быть более 150 символов, время приготовление не может быть менее минуты, ингредиенты в рецепте не должны повторятся. Вся валидация происходит на уровне моделей и в сериализаторах.


### Авторы:
backend - [Клинцова Анастасия](https://github.com/yanastasya)

frontend - Яндекс.Практикум
