from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class Student(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    is_banned = models.BooleanField(default=False)
    banned_date = models.DateField(null=True)
    is_collaborator = models.BooleanField(null=True, default=False)
    following_books = models.ManyToManyField(
        "books.Book", through="students.Following", related_name="following_students"
    )


class Following(models.Model):
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE)
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)
