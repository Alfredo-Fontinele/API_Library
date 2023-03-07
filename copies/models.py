from django.db import models

class Copy(models.Model):
    class Meta:
        ordering = ["id"]
        
    qtd_books = models.PositiveIntegerField()
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    users_borrowed = models.ManyToManyField(
        'users.User',
        through='copies.Borrow',
        related_name='copies_borrowed'
    )

class Borrow(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    copy = models.ForeignKey('copies.Copy', on_delete=models.CASCADE)
