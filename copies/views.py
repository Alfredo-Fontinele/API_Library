from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from django.shortcuts import get_object_or_404
from books.models import Book
from books.permissions import IsCollaboratorOrNot
from .models import Copy
from .serializers import CopySerializer

# Create your views here.


class CopiesView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCollaboratorOrNot]
    serializer_class = CopySerializer
    queryset = Copy.objects.all()

    def perform_create(self, serializer):
        book = get_object_or_404(Book, id=self.request.data["book_id"])

        return serializer.save(book_id=self.request.data["book_id"])
