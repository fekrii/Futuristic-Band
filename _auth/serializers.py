from sqlite3 import DataError

from django.contrib.auth.hashers import make_password
from django.db import transaction, IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import serializers, exceptions
from _auth.models import CustomUser, UserProfile


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "phone",
            "activated"
        ]
        extra_kwargs = {"password": {"write_only": True}}

class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = [
            "user",
            "firstName",
            "lastName",
            "gender",
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
                activated=True
            )
            if user:
                user.save()
                try:
                    new_profile = UserProfile.objects.create(
                        user=user,
                        firstName=validated_data["firstName"],
                        lastName=validated_data["lastName"],
                        gender=validated_data["gender"],
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


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if user.activated == True:
            return token
        else:
            raise exceptions.PermissionDenied()

    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        try:
            account = CustomUser.objects.get(email=attrs['email'])
            self.user = CustomUserSerializer(account)
            data['user'] = self.user.data

            success = True
            message = 'user logged successfully'
        except Exception as e:
            success = False
            message = e

        response = {'success': success, 'data': data, 'message': message}
        return response


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
