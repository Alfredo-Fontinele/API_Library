from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializer import BookSerializer
from .models import Book

class BookView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer 
    lookup_url_kwarg = "book_id"
