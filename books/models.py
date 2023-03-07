from django.db import models

class Book(models.Model):
    class Meta:
        ordering = ["id"]
    
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
