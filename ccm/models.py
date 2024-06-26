from django.db import models
import uuid
from user_management.models import User

# Create your models here.
class WilayaRepresentative(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    wilaya = models.CharField(max_length=50, blank=False, null=False)
    mkoa = models.CharField(max_length=50, blank=False, null=False)
    date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    wilaya_code = models.CharField(max_length=4, unique=True)
    representative = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.wilaya} - {self.representative}"
    
    class Meta:
        db_table = 'representative'


class Objective(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    objective = models.CharField(max_length=200)
    representative = models.ForeignKey(WilayaRepresentative, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        db_table = 'objective'
