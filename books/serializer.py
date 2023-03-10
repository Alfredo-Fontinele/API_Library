from rest_framework import serializers
from .models import Book
from rest_framework.validators import UniqueValidator

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'description'
        ]
        read_only_fields=[
            'id'
        ]

    def create(self, validated_data):
        return Book.objects.create(**validated_data)
    
    def update(self, instance: Book, validated_data: dict) -> Book:
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
