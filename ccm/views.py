from django.shortcuts import render
from mtaa import tanzania
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from ccm.serializers import RepresentativeSerializer
from .models import *

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

class RepresentativeUpdateView(APIView):

    def post(self, request):
        #Get email of the requested wilaya
        email = request.data.get('email')

        #Get the wilaya
        wilaya = request.data.get('wilaya')

        #Get the ccm_number
        ccm_number = request.data.get('ccm_number')

        #Check if the email is already used in another wilaya
        if WilayaRepresentative.objects.filter(email=email).exclude(wilaya=wilaya).exists():
            return Response({'error': 'Email is already used in another wilaya'}, status=status.HTTP_400_BAD_REQUEST)
        
        if WilayaRepresentative.objects.filter(ccm_number=ccm_number).exclude(wilaya=wilaya).exists():
            return Response({'error': "CCM number duplicate"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = RepresentativeSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            # Update the status to True
            instance.status = True
            instance.save()
            return Response({'success': True, 'representative': serializer.data})
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
