from rest_framework import serializers
from .models import Copy, Borrow
from books.serializer import BookSerializer
import datetime


class CopySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Copy
        fields = ["id", "qtd_books", "book_id", "is_avaliable"]

    def create(self, validated_data):
        existed_copie = Copy.objects.filter(book_id=validated_data["book_id"]).first()
        if existed_copie:
            for key, value in validated_data.items():
                if key == "qtd_books":
                    copies_result = value + existed_copie.qtd_books
                    setattr(existed_copie, key, copies_result)
        if existed_copie.qtd_books > 0:
            existed_copie.is_avaliable = True

        existed_copie.save()
        return existed_copie

        return Copy.objects.create(**validated_data)


class BorrowSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Borrow
        fields = [
            "id",
            "student_id",
            "copy_id",
            "borrowed_at",
            "return_date",
            "qtd_borrowed",
        ]
        read_only_fields = ["copy", "borrowed_at", "return_date"]

    def create(self, validated_data):
        borrow = Borrow.objects.create(**validated_data)
        copy = Copy.objects.get(id=validated_data.get("copy_id"))

        borrow.return_date += datetime.timedelta(days=5)
        while (
            borrow.return_date.isoweekday() == 3 or borrow.return_date.isoweekday() == 4
        ):
            borrow.return_date += datetime.timedelta(days=1)
        if copy.qtd_books < validated_data["qtd_borrowed"]:
            raise serializers.ValidationError(
                {"message": "Borrowed Quantity Bigger Them Quantity Avaliable"}
            )
        copy.qtd_books -= validated_data["qtd_borrowed"]
        if copy.qtd_books == 0:
            copy.is_avaliable = False

        copy.save()
        borrow.save()
        return borrow
