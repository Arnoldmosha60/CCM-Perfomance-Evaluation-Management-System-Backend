from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import UserSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token


class RegisterView(APIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            if User.objects.filter(email=email).exists():
                return Response(
                    {"error": "A user with this email already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            response = {
                'success': True,
                'message': 'User registered successfully',
                'user': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST,)


class LoginUser(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            user_id = User.objects.get(email=email)
            user_info = UserSerializer(instance=user_id, many=False).data
            token, created = Token.objects.get_or_create(user=user)
            response = {
                'token': token.key,
                'user': user_info,
                'success': True
            }
            return Response(response)
        else:
            response = {
                'msg': 'Invalid username or password',
            }
            return Response(response)


class GetUser(APIView):
    @staticmethod
    def get(request, query_type):
        if query_type == 'single':
            try:
                user_id = request.GET.get('user_id')
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'message': 'User Does Not Exist'})
            return Response(UserSerializer(instance=user, many=False).data)
        elif query_type == 'all':
            queryset = User.objects.all()
            return Response(UserSerializer(instance=queryset, many=True).data)
        else:
            return Response({'message': 'Wrong Request!'})


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = IsAuthenticated

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(APIView):
    permission_classes = AllowAny

    @staticmethod
    def post(request):
        username = request.data("username")
        email = request.data("email")
        contact = request.data("contact")
        location = request.data("location")
        if contact:
            try:
                query = User.objects.get(contact=contact)
                query.username = username
                query.email = email
                query.location = location
                query.save()
                return Response({'save': True, "user": UserSerializer(instance=query, many=False).data})
            except User.DoesNotExist:
                return Response({'message': 'You can not change the email'})
        else:
            return Response({'message': 'Not Authorized to Update This User'})


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # Perform logout actions here if needed
            request.user.auth_token.delete()  # Example: Deleting the user's auth token

            # Construct the response message
            message = {'detail': 'Logged out successfully'}
            return redirect('http://127.0.0.1:5500/pages/registration/login.html', message)
        except Exception as e:
            # Handle any exceptions gracefully
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

