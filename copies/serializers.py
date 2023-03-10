from rest_framework import serializers
from .models import Copy, Borrow
from books.serializer import BookSerializer


class CopySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Copy
        fields = ["id", "qtd_books", "book_id"]

    def create(self, validated_data):
        existed_copie = Copy.objects.filter(book_id=validated_data["book_id"]).first()
        if existed_copie:
            for key, value in validated_data.items():
                if key == "qtd_books":
                    copies_result = value + existed_copie.qtd_books
                    setattr(existed_copie, key, copies_result)

            existed_copie.save()
            return existed_copie

        return Copy.objects.create(**validated_data)
