
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Wifix import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'plans', views.PlanViewSet)
router.register(r'user-plans', views.UserPlanViewSet)
router.register(r'hotspots', views.HotspotViewSet)
router.register(r'sessions', views.SessionViewSet)
router.register(r'transactions', views.TransactionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', TemplateView.as_view(template_name="Wifix/index.html"), name='index'),
path('charge/', views.charge, name='charge'),

    path('select_plan/', views.select_plan, name='select_plan'),
    path('create_checkout_session/<int:plan_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
