from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializer import BookSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Book
from .permissions import IsCollaboratorOrNot

class BookView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCollaboratorOrNot]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    

class BookDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer 
    lookup_url_kwarg = "book_id"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCollaboratorOrNot]
