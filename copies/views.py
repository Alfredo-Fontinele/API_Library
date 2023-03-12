from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, serializers
from django.shortcuts import get_object_or_404
from books.models import Book
from rest_framework.permissions import IsAuthenticated
from books.permissions import IsCollaboratorOrNot
from .models import Copy, Borrow
from .serializers import CopySerializer, BorrowSerializer
from students.models import Student
from rest_framework.views import APIView, Response, Request, status
import datetime


# Create your views here.


class CopiesView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCollaboratorOrNot]
    serializer_class = CopySerializer
    queryset = Copy.objects.all()

    def perform_create(self, serializer):
        book = get_object_or_404(Book, id=self.request.data["book_id"])

        return serializer.save(book_id=self.request.data["book_id"])


class BorrowView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsCollaboratorOrNot]
    serializer_class = BorrowSerializer
    queryset = Borrow.objects.all()
    lookup_url_kwarg = "copy_id"

    def get_queryset(self):
        if self.request.user.is_collaborator:
            return Borrow.objects.all()
        for borrows in Borrow.objects.all():
            if borrows.student_id != self.request.user.id:
                raise serializers.ValidationError(
                    {
                        "message": "You Must Have A Borrow Or Be Collaborator To List Borrows"
                    }
                )
            if borrows.student_id == self.request.user.id:
                return Borrow.objects.filter(student_id=self.request.user.id)

    def perform_create(self, serializer):
        copy = get_object_or_404(Copy, id=self.request.data["copy_id"])
        student = get_object_or_404(Student, id=self.request.data["student_id"])

        if student.is_banned == True:
            raise serializers.ValidationError(
                {
                    "message": "You Are Banned. Return Your Borrowed Books and Wait 5 Days"
                }
            )

        for borrows in Borrow.objects.filter(student_id=student.id):
            if borrows.return_date < datetime.date.today():
                student.is_banned = True
                student.banned_date = datetime.date.today()
                student.save()
                raise serializers.ValidationError(
                    {
                        "You Borrows Not Returned At The Correct Day. You Have Been Banned"
                    }
                )
        if Borrow.objects.filter(
            student_id=student.id
        ) is False and datetime.date.today() >= student.banned_date + datetime.timedelta(
            days=5
        ):
            student.is_banned = False
            student.save()

        return serializer.save(
            student_id=student.id,
            copy_id=copy.id,
        )


class BorrowDevolution(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, borrow_id) -> Response:
        borrow = get_object_or_404(Borrow, id=borrow_id)
        copy_to_att = Copy.objects.get(id=borrow.copy_id)
        student = Student.objects.get(id=borrow.student_id)
        copy_to_att.qtd_books += borrow.qtd_borrowed
        copy_to_att.is_avaliable = True

        copy_to_att.save()
        borrow.delete()

        if borrow.return_date < datetime.date.today():
            student.is_banned = True
            student.banned_date = datetime.date.today()
            student.save()
            return Response(
                {
                    "message": "Borrowed Books Returned! But You Were Late. Your Account is Now Banned, Return All Your Borrows And Wait 5 Days"
                },
                status=status.HTTP_202_ACCEPTED,
            )

        return Response(
            {"message": "Borrowed Books Returned!"}, status=status.HTTP_202_ACCEPTED
        )
