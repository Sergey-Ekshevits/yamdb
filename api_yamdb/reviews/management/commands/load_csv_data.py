import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Загрузка данных из csv файла в БД'

    def handle(self, *args, **options):
        with open('static/data/users.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                users = CustomUser(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    bio=row['bio'],
                    role=row['role'],
                    first_name=row['first_name'],
                    last_name=row['last_name'])
                users.save()
            self.stdout.write(self.style.SUCCESS(
                'static/data/users.csv загружен в базу данных'))

        with open('static/data/category.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                category = Category(
                    name=row['name'],
                    slug=row['slug'])
                category.save()
            self.stdout.write(self.style.SUCCESS(
                'static/data/category.csv загружен в базу данных'))

        with open('static/data/genre.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                genre = Genre(
                    name=row['name'],
                    slug=row['slug'])
                genre.save()
            self.stdout.write(self.style.SUCCESS(
                'static/data/genre.csv загружен в базу данных'))

        with open('static/data/titles.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                category = Category.objects.get(id=row['category'])
                titles = Title(
                    name=row['name'],
                    year=row['year'],
                    category=category)
                titles.save()
            self.stdout.write(self.style.SUCCESS(
                'static/data/titles.csv загружен в базу данных'))

        with open('static/data/genre_title.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                title = Title.objects.get(id=row['title_id'])
                genre = Genre.objects.get(id=row['genre_id'])
                title.genre.add(genre)
            self.stdout.write(self.style.SUCCESS(
                'static/data/genre_title.csv загружен в базу данных'))

        with open('static/data/review.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                author = CustomUser.objects.get(id=row['author'])
                title = Title.objects.get(id=row['title_id'])
                review = Review(
                    text=row['text'],
                    score=row['score'],
                    pub_date=row['pub_date'],
                    author=author,
                    title=title)
                review.save()
            self.stdout.write(self.style.SUCCESS(
                'static/data/review.csv загружен в базу данных'))

        with open('static/data/comments.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                review = Review.objects.get(id=row['review_id'])
                author = CustomUser.objects.get(id=row['author'])
                comments = Comment(
                    text=row['text'],
                    review=review,
                    pub_date=row['pub_date'],
                    author=author)
                comments.save()
            self.stdout.write(self.style.SUCCESS(
                'static/data/comments.csv загружен в базу данных'))
