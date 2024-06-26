from django.shortcuts import render
from mtaa import tanzania
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from ccm.serializers import RepresentativeSerializer, ObjectiveSerializer
from user_management.serializers import UserSerializer
from .models import *
from django.shortcuts import get_object_or_404
import random
import logging
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()

# Create your views here.
class GetMikoa(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        mikoa = list(tanzania)  # Get all regions
        wilaya = {region: list(tanzania.get(region).districts) for region in mikoa}
        kata = {region: {district: list(tanzania.get(region).districts.get(district).wards) for district in wilaya[region]} for region in mikoa}
        
        total_mikoa = len(mikoa)
        total_wilaya = sum(len(districts) for districts in wilaya.values())
        total_kata = sum(len(wards) for district_wards in kata.values() for wards in district_wards.values())

        response = {
            'mikoa': mikoa,
            'wilaya': wilaya,
            'kata': kata,
            'total_mikoa': total_mikoa,
            'total_wilaya': total_wilaya,
            'total_kata': total_kata,
            'success': True
        }
        return Response(response)

class AddWilayaRepresentativeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    wilaya_representative_model = WilayaRepresentative
    user_model = User
    representative_serializer = RepresentativeSerializer
    user_serializer_class = UserSerializer

    def generate_unique_code(self):
        while True:
            code = f"{random.randint(1, 100):04d}"  # Generate a 4-digit code
            if not self.wilaya_representative_model.objects.filter(wilaya_code=code).exists():
                return code

    def post(self, request):
        # Get data from the request
        name = request.data.get('name')
        email = request.data.get('email')
        ccm_number = request.data.get('ccm_number')
        contact = request.data.get('contact')
        wilaya = request.data.get('wilaya')
        mkoa = request.data.get('mkoa')

        # Validate email uniqueness across wilayas
        if self.wilaya_representative_model.objects.filter(representative__email=email).exclude(wilaya=wilaya).exists():
            return Response({'error': 'Email is already used in another wilaya'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate CCM number uniqueness across wilayas
        if self.wilaya_representative_model.objects.filter(representative__ccm_number=ccm_number).exclude(wilaya=wilaya).exists():
            return Response({'error': "CCM number duplicate"}, status=status.HTTP_400_BAD_REQUEST)

        # Create or update the User
        user_data = {
            'fullname': name,
            'email': email,
            'ccm_number': ccm_number,
            'contact': contact,
        }

        try:
            user, created = self.user_model.objects.update_or_create(email=email, defaults=user_data)
            print(user)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a unique wilaya code
        wilaya_code = self.generate_unique_code()

        # Create or update the WilayaRepresentative
        representative_data = {
            'wilaya': wilaya,
            'mkoa': mkoa,
            'status': True,
            'wilaya_code': wilaya_code,
            'representative': user.id
        }

        serializer = self.representative_serializer(data=representative_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            userr = self.user_model.objects.get(id=user.id)
            user_serializer = self.user_serializer_class(userr)
            return Response({'success': True, 'representative': serializer.data, 'user': user_serializer.data}, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class RepresentativeListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RepresentativeSerializer
    representative_model = WilayaRepresentative
    user_model = User
    user_serializer_class = UserSerializer

    def get(self, request):
        representatives = self.representative_model.objects.all()
        serialized_data = []
        
        for representative in representatives:
            # Serialize the representative data
            representative_serializer = self.serializer_class(representative)
            representative_data = representative_serializer.data
            
            # Fetch the associated User object 
            user = self.user_model.objects.get(email=representative.representative)
            user_serializer = self.user_serializer_class(user)  # Serialize the User object
            
            # Append user data to representative data
            representative_data['user'] = user_serializer.data
            
            serialized_data.append(representative_data)
        
        return Response({"success": True, 'data': serialized_data}, status=status.HTTP_200_OK)


class ObjectiveCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = ObjectiveSerializer
    objective_model = Objective
    representative_model = WilayaRepresentative

    def post(self, request):
        try:
            # Extract representative_id from request data
            representative_id = request.data.get('representative_id')
            representative = get_object_or_404(self.representative_model, id=representative_id)

            # Extract objectives from request data
            objectives = request.data.get('objectives', [])

            created_objectives = []
            for objective_text in objectives:
                objective_instance = self.objective_model.objects.create(
                    objective=objective_text,
                    representative=representative
                )
                created_objectives.append(objective_instance)

            # Serialize the created objectives for response
            serializer = self.serializer_class(created_objectives, many=True)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ObjectiveListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = ObjectiveSerializer
    model = Objective

    def get(self, request, representative_id):
        try:
            # Filter objectives by representative_id
            objectives = self.model.objects.filter(representative=representative_id)
            if not objectives.exists():
                return Response({'error': 'No objectives found for the specified representative'}, status=status.HTTP_404_NOT_FOUND)
            # Serialize the filtered objectives for response
            serializer = self.serializer_class(objectives, many=True)
            return Response({'success': True, 'objectives': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


