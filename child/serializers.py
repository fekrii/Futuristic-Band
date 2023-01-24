from rest_framework import serializers, exceptions
from _auth.serializers import CustomUserSerializer
from .models import ChildProfile
from django.db import transaction, IntegrityError
from django.contrib.auth.hashers import make_password
from sqlite3 import DataError
from rest_framework.exceptions import ValidationError
from _auth.models import CustomUser
from parent.serializers import ParentProfileSerializer
from school.serializers import SchoolProfileSerializer
from parent.models import ParentProfile
from school.models import School

class ChildProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    parent = ParentProfileSerializer(read_only=True)
    school = SchoolProfileSerializer(read_only=True)
    banned_food = serializers.JSONField()
    class Meta:
        model = ChildProfile
        fields = [
            "user",
            "parent",
            "school",
            "firstName",
            "lastName",
            "birthDate",
            "child_at",
            "banned_food",
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
                    parent = ParentProfile.objects.get(id=user_input_data["parent"])
                    school = School.objects.get(id=user_input_data["school"])
                    new_profile = ChildProfile.objects.create(
                        user=user,
                        parent=parent,
                        school=school,
                        firstName=validated_data["firstName"],
                        lastName=validated_data["lastName"],
                        birthDate=validated_data["birthDate"],
                        child_at=validated_data["child_at"],
                        banned_food=validated_data["banned_food"]
                    )
                    return new_profile
                except:
                    IntegrityError("A user with that email already exists"),
                    DataError("The data provided is not valid")
            else:
                raise ValidationError("Serializer could not create a user object")

