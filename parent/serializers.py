from rest_framework import serializers, exceptions
from _auth.serializers import CustomUserSerializer
from .models import ParentProfile
from django.db import transaction, IntegrityError
from django.contrib.auth.hashers import make_password
from sqlite3 import DataError
from rest_framework.exceptions import ValidationError
from _auth.models import CustomUser

class ParentProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = ParentProfile
        fields = [
            "user",
            "firstName",
            "lastName",
            "parent_type",
            "birthDate",
            "address",
            "jobTitle",
            "nationality",
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
                    new_profile = ParentProfile.objects.create(
                        user=user,
                        firstName=validated_data["firstName"],
                        lastName=validated_data["lastName"],
                        parent_type=validated_data["parent_type"],
                        birthDate=validated_data["birthDate"],
                        address=validated_data["address"],
                        jobTitle=validated_data["jobTitle"],
                        nationality=validated_data["nationality"]
                    )
                    return new_profile
                except:
                    IntegrityError("A user with that email already exists"),
                    DataError("The data provided is not valid")
            else:
                raise ValidationError("Serializer could not create a user object")

