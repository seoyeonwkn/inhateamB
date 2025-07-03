from rest_framework import serializers
from .models import Badge, UserBadge, BadgeLog

class BadgeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadgeLog
        fields = ['created_at', 'reason']


class BadgeSerializer(serializers.ModelSerializer):
    logs = BadgeLogSerializer(source='awarded_users__logs', many=True, read_only=True)

    class Meta:
        model = Badge
        fields = [
            'id', 'name', 'description',
            'condition_description', 'image_url', 'category',
            'logs'
        ]


class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)

    class Meta:
        model = UserBadge
        fields = ['id', 'user', 'badge', 'awarded_at']
