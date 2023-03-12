from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from .models import Student, Following
from books.models import Book
from django.shortcuts import get_object_or_404
from .serializers import StudentSerializer, FollowingSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsStudent, IsTheSameStudent
from rest_framework.validators import ValidationError
from django.core.mail import send_mail
from django.conf import settings

class StudentView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    lookup_url_kwarg = "student_id"


class FollowingView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = FollowingSerializer
    queryset = Following.objects.all()

    def perform_create(self, serializer):
        book = get_object_or_404(Book, id=self.kwargs.get("book_id"))

        if Following.objects.filter(book=book, student=self.request.user):
            raise ValidationError({"message": f"You Already Follow {book.title}"})

        following = serializer.save(student=self.request.user, book=book)
        subject = f'Você está agora es´ta seguindo {book.title}'
        message = f"Olá {self.request.user.username}, você agora está seguindo {book.title}. Obrigado pelo seu interesse!"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [self.request.user.email]
        send_mail(subject, message, from_email, recipient_list)
        return following


class FollowingDetailView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsTheSameStudent]
    serializer_class = FollowingSerializer
    queryset = Following.objects.all()
    lookup_url_kwarg = "following_id"

    def perform_destroy(self, instance):
        following = get_object_or_404(Following, id=self.kwargs.get("following_id"))
        return instance
