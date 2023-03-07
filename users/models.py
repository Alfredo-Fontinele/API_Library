from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_banned = models.BooleanField(default=False)
    is_student = models.BooleanField(null=True, default=True)
    is_collaborator = models.BooleanField(null=True, default=False)
    books_following = models.ManyToManyField(
        'books.Book',
        through='users.Following',
        related_name='users_following'
    )

class Following(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
