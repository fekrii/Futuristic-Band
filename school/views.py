

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError, DataError
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SchoolProfileSerializer
from .models import School

@api_view(["POST"])
def register_school(request):
    """
    Create New School
    """
    with transaction.atomic():

        if ('user_data' in request.data) and ('profile' in request.data):
            serializer = SchoolProfileSerializer(
                data=request.data['profile'],
                context={
                    'user_data': request.data['user_data']
                }
            )
        else:
            return Response({
                'success': False,
                'data': "User Data must be provided in the request",
                'message': "failed"
            }, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response({
                    'success': True,
                    'data': serializer.data,
                    'message': "User created successfully"
                }, status=status.HTTP_201_CREATED)

            except ValidationError as e:
                # Exceptions raised by UserProfileSerializer
                # ValidationError: in case of any field errors.
                return Response({
                    'success': False,
                    'data': str(e),
                    'message': "User data is not valid"
                }, status=status.HTTP_400_BAD_REQUEST)

            except IntegrityError as e:
                # IntegrityError: an _auth with the same email address already exists
                return Response({
                    'success': False,
                    'data': str(e),
                    'message': "User already exists with the same email address"
                }, status=status.HTTP_400_BAD_REQUEST)
            except DataError as e:
                # DataError: in case any CharField data exceeds the max_length
                return Response({
                    'success': False,
                    'data': str(e),
                    'message': "User data is not valid"
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'success': False,
                'data': serializer.errors,
                'message': "User object not created"
            }, status=status.HTTP_400_BAD_REQUEST)

class SchoolView(APIView):
    def get(self, request):
        school = School.objects.get(user=self.request.user)
        serializer = SchoolProfileSerializer(school)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': f"Data for school : {self.request.user.id} Retrieved Successfully"
        })

    def put(self, request):
        school = School.objects.get(user=self.request.user)
        serializer = SchoolProfileSerializer(school, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': serializer.data,
                'message': f"Data for school : {self.request.user.id} Updated Successfully"
            })
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
