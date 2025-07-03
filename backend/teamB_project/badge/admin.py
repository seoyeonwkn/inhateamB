from django.contrib import admin
from .models import Badge, UserBadge, BadgeLevel, BadgeLog

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'category']
    search_fields = ['name']
    list_filter = ['category', 'level']


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'awarded_at']
    search_fields = ['user__login_id', 'badge__name']
    list_filter = ['awarded_at']


@admin.register(BadgeLevel)
class BadgeLevelAdmin(admin.ModelAdmin):
    list_display = ['badge', 'level', 'title']
    search_fields = ['badge__name', 'title']
    list_filter = ['level']


@admin.register(BadgeLog)
class BadgeLogAdmin(admin.ModelAdmin):
    list_display = ['user_badge', 'reason', 'created_at']
    search_fields = ['user_badge__user__login_id', 'reason']
    list_filter = ['created_at']


