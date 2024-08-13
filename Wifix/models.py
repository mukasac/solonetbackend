# wifi_app/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Plan(models.Model):
    name = models.CharField(max_length=50)
    duration = models.DurationField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class UserPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()

    def is_active(self):
        return self.start_time <= timezone.now() <= self.end_time

class Hotspot(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotspot = models.ForeignKey(Hotspot, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    data_used = models.BigIntegerField(default=0)  # in bytes

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('success', 'Success'), ('failed', 'Failed')])

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_payment_intent_id = models.CharField(max_length=255)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.user} - {self.plan.name}'
