from django.http import HttpResponse
# wifi_app/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.utils import timezone
from .models import Plan, UserPlan, Hotspot, Session, Transaction
from .serializers import UserSerializer, PlanSerializer, UserPlanSerializer, HotspotSerializer, SessionSerializer, TransactionSerializer
from django.contrib.auth.models import User
from django.views.generic import TemplateView
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY


def charge(request):
    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        try:
            charge = stripe.Charge.create(
                amount=5000,  # amount in cents
                currency='usd',
                description='Example charge',
                source=token,
            )
            return render(request, 'charge.html', {'amount': 5000})
        except stripe.error.StripeError as e:
            return render(request, 'payment_error.html', {'error': str(e)})

    return render(request, 'payment_form.html', {'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        user = User.objects.filter(username=request.data['username']).first()
        if user and user.check_password(request.data['password']):
            login(request, user)
            return Response({'detail': 'Login successful'})
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout(request)
        return Response({'detail': 'Logout successful'})

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class UserPlanViewSet(viewsets.ModelViewSet):
    queryset = UserPlan.objects.all()
    serializer_class = UserPlanSerializer

    @action(detail=False, methods=['post'])
    def select_plan(self, request):
        user = request.user
        plan = Plan.objects.get(id=request.data['plan_id'])
        end_time = timezone.now() + plan.duration
        user_plan = UserPlan.objects.create(user=user, plan=plan, end_time=end_time)
        return Response(UserPlanSerializer(user_plan).data)

class HotspotViewSet(viewsets.ModelViewSet):
    queryset = Hotspot.objects.all()
    serializer_class = HotspotSerializer

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    class IndexView(TemplateView):
        template_name = "Wifix/index.html"

def select_plan(request):
    plans = Plan.objects.all()
    return render(request, 'select_plan.html', {'plans': plans})

def create_checkout_session(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': plan.name,
                },
                'unit_amount': int(plan.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://yourdomain.com/success',
        cancel_url='https://yourdomain.com/cancel',
    )
    return redirect(session.url, code=303)

@csrf_exempt
def payment_success(request):
    # Logic to handle a successful payment, e.g., saving the payment details to your database
    return render(request, 'payment_success.html')

# views.py

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session(session)

    return HttpResponse(status=200)

def handle_checkout_session(session):
    # Logic to update the user's payment status in the database
    pass
