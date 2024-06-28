from django.shortcuts import render
from mtaa import tanzania
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from ccm.serializers import RepresentativeSerializer, ObjectiveSerializer, TargetSerializer, IndicatorSerializer
from user_management.serializers import UserSerializer
from .models import *
from django.shortcuts import get_object_or_404
import random
import logging
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()

# models
# user_model = User
# objective_model = Objective
# Indicator_model = Indicator
# representative_model = WilayaRepresentative

# serializers
# user_serializer = UserSerializer
# objective_serializer = ObjectiveSerializer
# representative_serializer = RepresentativeSerializer
# indicator_serializer = IndicatorSerializer

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
            code = f"{random.randint(1, 100000):05d}"  # Generate a 4-digit code
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
            'representative': str(user.id)
        }
        print(representative_data)
        serializer = self.representative_serializer(data=representative_data, partial=True)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            userr = self.user_model.objects.get(id=user.id)
            user_serializer = self.user_serializer_class(userr)
            return Response({'success': True, 'representative': serializer.data, 'user': user_serializer.data}, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
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
    representative_serializer = RepresentativeSerializer
    objective_model = Objective
    representative_model = WilayaRepresentative
    user_model = User

    def generate_unique_code(self):
        while True:
            code = f"{random.randint(1, 100000):05d}"  # Generate a 4-digit code
            if not self.objective_model.objects.filter(objective_code=code).exists():
                return code

    def post(self, request):
        try:
            admin = request.user
            adminn = get_object_or_404(self.user_model, email=admin)
            # Extract representative_id from request data
            representative_id = request.data.get('representative_id')
            representative = get_object_or_404(self.representative_model, id=representative_id)

            # Extract objectives from request data
            objectives = request.data.get('objectives', [])

            created_objectives = []
            for objective_text in objectives:
                objective_instance = self.objective_model.objects.create(
                    objective=objective_text,
                    representative=representative,
                    objective_code=self.generate_unique_code(),
                    created_by=adminn
                )
                created_objectives.append(objective_instance)

            # Serialize the created objectives for response
            serializer = self.serializer_class(created_objectives, many=True)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Error in ObjectiveCreateView: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        try:
            objectives = self.objective_model.objects.all()
            objective_data = []

            for objective in objectives:
                objective_dict = self.serializer_class(objective).data

                #Fetch representative
                rep = self.representative_model.objects.get(id=objective.representative_id)
                rep_serializer = self.representative_serializer(rep)
                rep_data = rep_serializer.data

                objective_dict['representative'] = rep_data
                objective_data.append(objective_dict)
            return Response({'success': True, 'data': objective_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Something went wrong: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ObjectiveListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = ObjectiveSerializer
    model = Objective
    representative_model = WilayaRepresentative

    def get(self, request, representative_id):
        try:
            # Fetch the representative by ID
            representative = get_object_or_404(self.representative_model, representative=representative_id)

            # Fetch objectives associated with the representative
            objectives = self.model.objects.filter(representative=representative.id)

            # Serialize the objectives
            serializer = self.serializer_class(objectives, many=True)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error in UserObjectivesView: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TargetCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TargetSerializer
    model = Target
    objective_model = Objective
    user_model = User

    def generate_unique_code(self):
        while True:
            code = f"{random.randint(1, 100000):05d}"  # Generate a 4-digit code
            if not self.model.objects.filter(target_code=code).exists():
                return code
    
    def post(self, request):
        try:
            admin = request.user
            adminn = get_object_or_404(self.user_model, email=admin)

            objective_id = request.data.get('objective_id')
            objective = get_object_or_404(self.objective_model, id=objective_id)

            targets = request.data.get('targets', [])

            created_targets = []
            for target in targets:
                instance = self.model.objects.create(
                    target=target,
                    objective=objective,
                    target_code=self.generate_unique_code(),
                    created_by=adminn
                )
                created_targets.append(instance)
        
            serializer = self.serializer_class(created_targets, many=True)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Error in TargetCreateView: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            targets = self.model.objects.all()
            target_data = []
            
            for target in targets:
                target_dict = self.serializer_class(target).data
                
                # Fetch related user data
                user = User.objects.get(id=target.created_by_id)
                user_data = {
                    'id': user.id,
                    'fullname': user.fullname,
                    'email': user.email,
                    'contact': user.contact, 
                    'ccm_number': user.ccm_number,
                }
                
                # Update created_by field in the serialized data
                target_dict['created_by'] = user_data
                
                target_data.append(target_dict)
            
            return Response({'success': True, 'data': target_data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': f'Something went wrong: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TargetListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TargetSerializer
    model = Target
    objective_model = Objective

    def get(self, request, objective_id):
        try:
            objective = get_object_or_404(self.objective_model, id=objective_id)
            targets = self.model.objects.filter(objective=objective)
            serializer = self.serializer_class(targets, many=True)
            print(serializer.data)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error in UserTargetsView: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class IndicatorCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = IndicatorSerializer
    target_model = Target
    model = Indicator
    user_model = User
    user_serializer = UserSerializer

    def generate_unique_code(self):
        while True:
            code = f"{random.randint(1, 100000):05d}"  # Generate a 4-digit code
            if not self.model.objects.filter(indicator_code=code).exists():
                return code
    
    def post(self,request):
        try:
            admin = request.user
            adminn = get_object_or_404(self.user_model, email=admin)

            target_id = request.data.get('target_id')
            target = get_object_or_404(self.target_model, id=target_id)

            indicators = request.data.get('indicators', [])

            created_indicators = []
            for indicator in indicators:
                instance = self.model.objects.create(
                    indicator=indicator,
                    target=target,
                    indicator_code=self.generate_unique_code(),
                    created_by=adminn
                )
                created_indicators.append(instance)
            
            serializer = self.serializer_class(created_indicators, many=True)

            return Response({
                'success': True, 
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Error in IndicatorCreateView: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            indicators = self.model.objects.select_related('created_by').all()
            serializer = self.serializer_class(indicators, many=True)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Something went wrong: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IndicatorListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = IndicatorSerializer
    model = Indicator
    target_model = Target

    def get(self, request, target_id):
        try:
            target = get_object_or_404(self.target_model, id=target_id)
            indicators = self.model.objects.filter(target=target)
            serializer = self.serializer_class(indicators, many=True)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error in UserIndicatorsView: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



