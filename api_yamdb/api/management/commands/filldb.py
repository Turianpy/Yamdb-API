import contextlib
import csv
from datetime import datetime

from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User
from django.shortcuts import get_object_or_404


class Command(BaseCommand):
    def handle(self, *args, **options):

        p = 'static/data/'

        with contextlib.ExitStack() as stack:
            categories = csv.DictReader(
                stack.enter_context(open(f'{p}category.csv', 'r'))
            )
            genres = csv.DictReader(
                stack.enter_context(open(f'{p}genre.csv', 'r'))
            )
            titles = csv.DictReader(
                stack.enter_context(open(f'{p}titles.csv', 'r'))
            )
            genre_title = csv.DictReader(
                stack.enter_context(open(f'{p}genre_title.csv', 'r'))
            )
            users = csv.DictReader(
                stack.enter_context(open(f'{p}users.csv', 'r'))
            )
            reviews = csv.DictReader(
                stack.enter_context(open(f'{p}review.csv', 'r'))
            )
            comments = csv.DictReader(
                stack.enter_context(open(f'{p}comments.csv', 'r'))
            )

            for row in categories:
                Category.objects.get_or_create(
                    id=int(row['id']),
                    name=row['name'],
                    slug=row['slug']
                )

            for row in genres:
                Genre.objects.get_or_create(
                    id=int(row['id']),
                    name=row['name'],
                    slug=row['slug']
                )

            for row in titles:
                Title.objects.get_or_create(
                    id=int(row['id']),
                    name=row['name'],
                    year=int(row['year']),
                    category=get_object_or_404(
                        Category,
                        id=int(row['category'])
                    )
                )

            for row in genre_title:
                GenreTitle.objects.get_or_create(
                    id=int(row['id']),
                    title=get_object_or_404(
                        Title,
                        id=int(row['title_id'])),
                    genre=get_object_or_404(
                        Genre,
                        id=int(row['genre_id'])
                    )
                )

            for row in users:
                User.objects.get_or_create(
                    id=int(row['id']),
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )

            for row in reviews:
                Review.objects.get_or_create(
                    id=int(row['id']),
                    title_id=int(row['title_id']),
                    text=row['text'],
                    author=get_object_or_404(
                        User,
                        id=int(row['author'])),
                    score=int(row['score']),
                    pub_date=datetime.fromisoformat(row['pub_date'])
                )

            for row in comments:
                Comment.objects.get_or_create(
                    id=int(row['id']),
                    review=get_object_or_404(
                        Review,
                        id=int(row['review_id'])),
                    author=get_object_or_404(
                        User,
                        id=int(row['author'])),
                    text=row['text'],
                    pub_date=datetime.fromisoformat(row['pub_date'])
                )


def main():
    command = Command()
    command.handle()


if __name__ == '__main__':
    main()
