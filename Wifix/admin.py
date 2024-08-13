# wifi_app/admin.py

from django.contrib import admin
from .models import Plan, UserPlan, Hotspot, Session, Transaction

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'price')
    search_fields = ('name',)

@admin.register(UserPlan)
class UserPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_time', 'end_time', 'is_active')
    list_filter = ('plan', 'start_time', 'end_time')
    search_fields = ('user__username', 'plan__name')

@admin.register(Hotspot)
class HotspotAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'location')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'hotspot', 'start_time', 'end_time', 'data_used')
    list_filter = ('hotspot', 'start_time')
    search_fields = ('user__username', 'hotspot__name')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'amount', 'timestamp', 'status')
    list_filter = ('status', 'plan', 'timestamp')
    search_fields = ('user__username', 'plan__name')

    admin.site.site_header = "Si-Wifi"
    admin.site.site_title = "Si-Wifi Administration"
    admin.site.index_title = "Welcome to Si-Wifi Administration"