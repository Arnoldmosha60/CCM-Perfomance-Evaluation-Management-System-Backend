from django.shortcuts import render
from mtaa import tanzania
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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
