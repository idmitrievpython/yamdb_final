import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Categories, Comments, Genre, Review, Title, User


class Command(BaseCommand):
    help = 'Load data from static'

    def handle(self, *args, **kwargs):
        """Открываю каждый файл по отдельности из-за несоответствия колонок."""
        with open(
                f'{settings.BASE_DIR}/static/data/users.csv',
                'r',
                encoding='utf-8'
        ) as csv_file:
            data = csv.reader(csv_file, delimiter=",")
            next(data)
            for row in data:
                User.objects.get_or_create(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6]
                )

        with open(
                f'{settings.BASE_DIR}/static/data/categories.csv',
                'r',
                encoding='utf-8'
        ) as csv_file:
            data = csv.reader(csv_file, delimiter=",")
            next(data)
            for row in data:
                Categories.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )

        with open(
                f'{settings.BASE_DIR}/static/data/genre.csv',
                'r',
                encoding='utf-8'
        ) as csv_file:
            data = csv.reader(csv_file, delimiter=",")
            next(data)
            for row in data:
                Genre.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )

        with open(
                f'{settings.BASE_DIR}/static/data/titles.csv',
                'r',
                encoding='utf-8'
        ) as csv_file:
            data = csv.reader(csv_file, delimiter=",")
            next(data)
            for row in data:
                Title.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category_id=row[3]
                )

        with open(
                f'{settings.BASE_DIR}/static/data/review.csv',
                'r',
                encoding='utf-8'
        ) as csv_file:
            data = csv.reader(csv_file, delimiter=",")
            next(data)
            for row in data:
                Review.objects.get_or_create(
                    id=row[0],
                    title_id=row[1],
                    text=row[2],
                    author_id=row[3],
                    score=row[4],
                    pub_date=row[5]
                )

        with open(
                f'{settings.BASE_DIR}/static/data/comments.csv',
                'r',
                encoding='utf-8'
        ) as csv_file:
            data = csv.reader(csv_file, delimiter=",")
            next(data)
            for row in data:
                Comments.objects.get_or_create(
                    id=row[0],
                    reviews_id=row[1],
                    text=row[2],
                    author_id=row[3],
                    pub_date=row[4]
                )
