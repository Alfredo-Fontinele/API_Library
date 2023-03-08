from django.db import models
import uuid

class Book(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
