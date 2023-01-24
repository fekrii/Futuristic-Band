from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError, DataError
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ChildProfileSerializer


@api_view(["POST"])
def register_child(request):
    """
    Create New child
    """
    with transaction.atomic():

        if ('user_data' in request.data) and ('profile' in request.data):
            serializer = ChildProfileSerializer(
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
