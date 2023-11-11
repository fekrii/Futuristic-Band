from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError, DataError
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ChildProfileSerializer, ChildWalletSerializer, ChildDaysOffSerializer
from rest_framework import generics
from .models import ChildWallet, ChildProfile, ChildDaysOff

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

# class ChildView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = ChildProfile.objects.all()
#     serializer_class = ChildProfileSerializer

class ChildView(APIView):
    def get(self, request, child_id):
        child = ChildProfile.objects.get(user_id=child_id)
        serializer = ChildProfileSerializer(child)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': f"Data for child {child_id} Retrieved Successfully"
        })

    def put(self, request, child_id):
        child = ChildProfile.objects.get(user_id=child_id)
        serializer = ChildProfileSerializer(child, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': serializer.data,
                'message': f"Data for child {child_id} Updated Successfully"
            })
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ChildWalletList(generics.ListCreateAPIView):
    queryset = ChildWallet.objects.all()
    serializer_class = ChildWalletSerializer
        
    def get_queryset(self, *args, **kwargs):
        wallet = super().get_queryset(*args, **kwargs).filter(
            child__user=self.request.data['child']

        )
        return wallet



class ChildListView(generics.ListCreateAPIView):
    queryset = ChildProfile.objects.all()
    serializer_class = ChildProfileSerializer 
    
    def get_queryset(self, *args, **kwargs):
        try:
            child = super().get_queryset(*args, **kwargs).filter(
            school__user=self.request.user

        )
            return child
        except:
            return super().get_queryset(*args, **kwargs)
class ChildWalletView(APIView):
    def get(self, request, child_id):
        wallet = ChildWallet.objects.filter(child_id=child_id)
        serializer = ChildWalletSerializer(wallet, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': f"wallet for child with id {child_id}"
        })
    
    def put(self, request, child_id):
        
        try:
            amount = request.data["amount"]
            wallet = ChildWallet.objects.filter(child_id=child_id)
            wallet.amount = amount
            serializer = ChildWalletSerializer(wallet, many=True)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': f"amount for child with id {child_id} has been updated to {amount}"
            })
        except:
            return Response({
                'success': False,
                'data': None,
                'message': "amount must be provided"
            })



class BannedFoodView(APIView):
    def get(self, request, child_id):
        child = ChildProfile.objects.get(id=child_id)
        return Response({
            'success': True,
            'data': child.banned_food,
            'message': f"banned food for child with id {child_id}"
        })
    
    def put(self, request, child_id):
        
        try:
            banned_food = request.data["banned_food"]
            child = ChildProfile.objects.get(id=child_id)
            child.banned_food = banned_food
            child.save()
            serializer = ChildProfileSerializer(child)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': f"banned food for child with id {child_id} has been updated"
            })
        except:
            return Response({
                'success': False,
                'data': None,
                'message': "banned_food must be provided"
            })


class ChildDaysOffView(APIView):
    def get(self, request, child_id):
        days_off = ChildDaysOff.objects.filter(child_id=child_id)
        serializer = ChildDaysOffSerializer(days_off, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': f"days off for child with id {child_id}"
        })
        
    def post(self, request, child_id):
        child = ChildProfile.objects.get(id=child_id)
        day = request.data["day"]
        reason = request.data["reason"] 
        day_off = ChildDaysOff.objects.create(child=child, day=day, reason=reason)
        serializer = ChildDaysOffSerializer(day_off)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': f"day off for child with id {child_id} Created Successfully"
        })
        
        
    # def put(self, request, child_id):
        
    #     try:
    #         amount = request.data["amount"]
    #         wallet = ChildWallet.objects.filter(child_id=child_id)
    #         wallet.amount = amount
    #         serializer = ChildWalletSerializer(wallet, many=True)
    #         return Response({
    #             'success': True,
    #             'data': serializer.data,
    #             'message': f"amount for child with id {child_id} has been updated to {amount}"
    #         })
    #     except:
    #         return Response({
    #             'success': False,
    #             'data': None,
    #             'message': "amount must be provided"
    #         })
