from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError, DataError
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ParentProfileSerializer
from rest_framework import generics, status
from child.models import ChildProfile
from child.serializers import ChildProfileSerializer
from parent.models import ParentProfile



@api_view(["POST"])
def register_parent(request):
    """
    Create New parent
    """
    with transaction.atomic():

        if ('user_data' in request.data) and ('profile' in request.data):
            serializer = ParentProfileSerializer(
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


class ParentChildListView(generics.ListAPIView):
    queryset = ChildProfile.objects.all()
    serializer_class = ChildProfileSerializer
    
    def get_queryset(self, *args, **kwargs):
        child = super().get_queryset(*args, **kwargs).filter(
            parent__user=self.request.user

        )
        return child

class ParentListView(generics.ListAPIView):
    queryset = ParentProfile.objects.all()
    serializer_class = ParentProfileSerializer

    def get_queryset(self, *args, **kwargs):
        try:
            childs = ChildProfile.objects.filter(school__user=self.request.user)
            parent = super().get_queryset(*args, **kwargs).filter(
                ChildParent__in=childs

            ).distinct()
            return parent
        except:
            return super().get_queryset(*args, **kwargs)
    
    
    
class ParentView(APIView):
    def get(self, request, parent_id):
        parent = ParentProfile.objects.get(user_id=parent_id)
        serializer = ParentProfileSerializer(parent)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': f"Data for parent {parent_id} Retrieved Successfully"
        })
        
    def put(self, request, parent_id):
        parent = ParentProfile.objects.get(user_id=parent_id)
        serializer = ParentProfileSerializer(parent, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': serializer.data,
                'message': f"Data for parent {parent_id} Updated Successfully"
            })
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# class ParentChildIDListView(APIView):
#     def get(self, request, parent_id):
#         childs = ChildProfile.objects.filter(parent_id=parent_id)
#         serializer = ChildProfileSerializer(childs, many=True)
#         return Response({
#             'success': True,
#             'data': serializer.data,
#             'message': f"Childs  for parent {parent_id} Retrieved Successfully"
#         })


class ParentChildIDListView(generics.ListAPIView):
    queryset = ChildProfile.objects.all()
    serializer_class = ChildProfileSerializer

    def get_queryset(self, *args, **kwargs):
        child = super().get_queryset(*args, **kwargs).filter(
            parent_id=self.kwargs['parent_id']

        )
        return child