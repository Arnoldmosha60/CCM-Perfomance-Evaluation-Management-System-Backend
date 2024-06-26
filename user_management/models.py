from django.contrib.auth.models import AbstractUser,  BaseUserManager
from django.db import models
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, fullname, ccm_number, contact, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, fullname=fullname, ccm_number=ccm_number, contact=contact, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, ccm_number, contact, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, fullname, contact, ccm_number, password, **extra_fields)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=12)
    ccm_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fullname", "ccm_number", "contact"]

    objects = CustomUserManager()  # Set the custom user manager

    def __str__(self):
        return str(self.email)

    class Meta:
        db_table = 'user'