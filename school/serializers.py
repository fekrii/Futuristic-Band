from rest_framework import serializers, exceptions
from _auth.serializers import CustomUserSerializer
from .models import School
from django.db import transaction, IntegrityError
from django.contrib.auth.hashers import make_password
from sqlite3 import DataError
from rest_framework.exceptions import ValidationError
from _auth.models import CustomUser

class SchoolProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = School
        fields = [
            "user",
            "name",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ['user']

    def create(self, validated_data):
        with transaction.atomic():
            user_input_data = self.context.get('user_data')
            user = CustomUser.objects.create(
                email=user_input_data['email'],
                password=make_password(user_input_data['password']),
                phone=user_input_data['phone'],

                # we can turn it to activated=False for security
                # (meaning that user must be activated from our side first before logging in)
                activated=False
            )
            if user:
                user.save()
                try:
                    new_profile = School.objects.create(
                        user=user,
                        name=validated_data["name"]
                    )
                    return new_profile
                except:
                    IntegrityError("A user with that email already exists"),
                    DataError("The data provided is not valid")
            else:
                raise ValidationError("Serializer could not create a user object")

