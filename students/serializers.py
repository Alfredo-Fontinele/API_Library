from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError


from .models import Student, Following


class StudentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=Student.objects.all(),
                message="A Student with that username already exists.",
            )
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=Student.objects.all(),
                message="Student with this email already exists.",
            )
        ],
    )

    def create(self, validated_data: dict) -> Student:
        return Student.objects.create_user(**validated_data)

    def update(self, instance: Student, validated_data: dict):
        for keys, value in validated_data.items():
            setattr(instance, keys, value)
        if "password" in validated_data.keys():
            instance.set_password(validated_data["password"])
        if "is_collborator" or "is_banned" in validated_data.keys():
            raise ValidationError(
                {"message": "is_collborator and is_banned cannot be changed!"}
            )

        instance.save()
        return instance

    class Meta:
        model = Student
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_banned",
            "is_collaborator",
        ]
        read_only_fields = ["is_banned", "is_collaborator"]
        extra_kwargs = {"password": {"write_only": True}}

class FollowingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    student = StudentSerializer(read_only=True)


    def create(self, validated_data):
        return Following.objects.create(**validated_data)
    
    
    class Meta:
        model = Following
        fields = ["id","student", "book"]
        read_only_fields = ["student", "book",]
        validators = []

    