# wifi_app/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Plan, UserPlan, Hotspot, Session, Transaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        extra_kwargs = {'password': {'write_only': True}}

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class UserPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlan
        fields = '__all__'

class HotspotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotspot
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'