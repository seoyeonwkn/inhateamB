from django.contrib import admin
from .models import Badge, UserBadge, BadgeLevel, BadgeLog

admin.site.register(Badge)
admin.site.register(UserBadge)
admin.site.register(BadgeLevel)
admin.site.register(BadgeLog)
