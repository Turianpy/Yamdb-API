import contextlib
import csv
from datetime import datetime

from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):

        with contextlib.ExitStack() as stack:
            categories = csv.DictReader(
                stack.enter_context(open('category.csv', 'r'))
            )
            genres = csv.DictReader(
                stack.enter_context(open('genre.csv', 'r'))
            )
            titles = csv.DictReader(
                stack.enter_context(open('titles.csv', 'r'))
            )
            genre_title = csv.DictReader(
                stack.enter_context(open('genre_title.csv', 'r'))
            )
            users = csv.DictReader(
                stack.enter_context(open('users.csv', 'r'))
            )
            reviews = csv.DictReader(
                stack.enter_context(open('reviews.csv', 'r'))
            )
            comments = csv.DictReader(
                stack.enter_context(open('comments.csv', 'r'))
            )

            for row in categories:
                Category.objects.create(
                    id=int(row['id']),
                    name=row['name'],
                    slug=row['slug']
                )

            for row in genres:
                Genre.objects.create(
                    id=int(row['id']),
                    name=row['name'],
                    slug=row['slug']
                )

            for row in titles:
                Title.objects.create(
                    id=int(row['id']),
                    name=row['name'],
                    year=int(row['year']),
                    category=int(row['category'])
                )

            for row in genre_title:
                GenreTitle.objects.create(
                    id=int(row['id']),
                    title=int(row['title_id']),
                    genre=int(row['genre_id'])
                )

            for row in users:
                User.objects.create(
                    id=int(row['id']),
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )

            for row in reviews:
                Review.objects.create(
                    id=int(row['id']),
                    title_id=int(row['title_id']),
                    text=row['text'],
                    author=int(row['author']),
                    score=int(row['score']),
                    pub_date=datetime.fromisoformat(row['pub_date'])
                )

            for row in comments:
                Comment.objects.create(
                    id=int(row['id']),
                    author=int(row['author']),
                    text=row['text'],
                    pub_date=datetime.fromisoformat(row['pub_date'])
                )


def main():
    command = Command()
    command.handle()


if __name__ == '__main__':
    main()
