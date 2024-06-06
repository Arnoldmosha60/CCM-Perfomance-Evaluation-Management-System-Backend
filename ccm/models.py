from django.db import models
import uuid

# Create your models here.
class WilayaRepresentative(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=50)
    wilaya = models.CharField(max_length=50, blank=False, null=False)
    mkoa = models.CharField(max_length=50, blank=False, null=False)
    contact = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    ccm_number = models.CharField(max_length=30, unique=True, blank=False, null=False)
    date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Name: {self.name}, wilaya: {self.wilaya}"
