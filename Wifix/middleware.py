# wifi_app/middleware.py

from django.utils import timezone
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import UserPlan

class PlanExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            active_plan = UserPlan.objects.filter(user=request.user, end_time__gt=timezone.now()).first()
            if not active_plan:
                logout(request)
                return JsonResponse({'message': 'Plan expired. Please login again.'}, status=401)
        return self.get_response(request)