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
    wilaya_code = models.CharField(max_length=5, unique=True)
    representative = models.ForeignKey(User, on_delete=models.CASCADE)

    def __repr__(self):
        return repr(self.id)
    
    class Meta:
        db_table = 'representative'


class Objective(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    objective = models.CharField()
    representative = models.ForeignKey(WilayaRepresentative, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    objective_code = models.CharField(max_length=5, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __repr__(self):
        return repr(self.id)
    
    class Meta:
        db_table = 'objective'


class Target(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    target = models.CharField()
    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    target_code = models.CharField(max_length=5, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __repr__(self):
        return repr(self.id)
    
    class Meta:
        db_table = 'target'


class Indicator(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    indicator = models.CharField()
    target = models.ForeignKey(Target, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    indicator_code = models.CharField(max_length=5, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    achievement_percentage = models.FloatField(default=0.0)

    def __repr__(self):
        return repr(self.id)

    class Meta:
        db_table = 'indicator'


class Activity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity = models.CharField()
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_code = models.CharField(max_length=5, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __repr__(self):
        return repr(self.id)
    
    class Meta:
        db_table = 'activity'
