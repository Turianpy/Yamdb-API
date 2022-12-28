from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    USER_ROLES = (
        (ADMIN, 'Администратор'),
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль', max_length=20,
        choices=USER_ROLES,
        default='user'
    )

    @property
    def is_admin(self):
        """Is the user a member of staff?."""
        return self.role == User.ADMIN

    @property
    def is_user(self):
        """Is the user a member of staff?."""
        return self.role == User.USER

    @property
    def is_moderator(self):
        """Is the user a member of staff?."""
        return self.role == User.MODERATOR
