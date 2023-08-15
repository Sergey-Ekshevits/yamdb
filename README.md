# Проект YaMDb

### :grey_question: О проекте
Проект YaMDb собирает отзывы пользователей на различные произведения.
Произведения делятся на категории, такие как "Фильм", "Музыка", "Книга". Список категорий может быть расширен. Каждому произведению может быть присвоен жанр или несколько жанров из предустановленных.
Благодарные или возмущённые пользователи могут оставить к произведениям текстовые отзывы и оценку от 1 до 10. Из пользовательских оценок формируется рейтинг произведения. К отзывам можно оставлять комментарии.
Пользователи имеют свой редактируемый профиль. Просматривать и редактировать все профили может только администратор. 

### :mechanical_arm: Возможности
* Регистрация пользователей с отправкой кода подтверждения на e-mail
* Права доступа: аноним, аутентифицированный пользователь, модератор, администратор
* Отзывы с оценками, комментарии к отзывам, рейтинг произведений
* Загрузка csv файлов с помощью management-команды

### :desktop_computer: Технологии
* Python
* Django 3.2
* Django REST
* JSON Web Token

### :arrow_forward: Деплой проекта
Клонировать репозиторий в командной строке:
```
git clone https://github.com/Djentie/api_yamdb
```
Установить виртуальное окружение:
```
python -m venv venv
```
Активировать виртуальное окружение:
```
source venv/Scripts/activate
```
Обновить pip:
```
python -m pip install --upgrade pip
```
Установить зависимости:
```
pip install -r requirements.txt
```
Применить миграции:
```
python manage.py migrate
```
Загрузить файлы csv в базу данных:
```
python manage.py load_csv_data
```
Запустить сервер:
```
python manage.py runserver
```

### Примеры
Примеры запросов можно посмотреть по [ссылке](http://127.0.0.1:8000/redoc/) после запуска сервера.

### :raising_hand_man: Авторы
* Азат Фаттахов https://github.com/Djentie
* Света Никифорова https://github.com/NikiSv
* Сергей Екшевиц https://github.com/Sergey-Ekshevits