from django.urls import path
from .views import *

urlpatterns = [
    path('register', RegisterView.as_view(), name="register"),
    path('login', LoginUser.as_view(), name="login"),
    path('logout/', LogoutView.as_view()),
    path('user-information/<slug:query_type>', GetUser.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('update-profile/', UpdateUserView.as_view()),
]
