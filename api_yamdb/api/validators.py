from rest_framework.exceptions import ValidationError
from users.models import User
import re

username_pattern = re.compile(r'^[\w.@+-]+\Z')


def validate_username(value):
    if value == 'me':
        raise ValidationError('Недопустимое имя пользователя')
    if not username_pattern.match(value):
        raise ValidationError(
            'Cringe username try again'
        )


def validate_username_or_email_exists(username, email):
    if User.objects.filter(username=username).exists():
        raise ValidationError(
            'Пользователь c таким именем '
            'уже зарегестрирован'
        )
    if User.objects.filter(email=email).exists():
        raise ValidationError(
            'Пользователь с такой почтой '
            'уже зарегестрирован'
        )
