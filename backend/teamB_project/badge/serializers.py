from rest_framework import serializers
from .models import Badge, UserBadge, BadgeLevel, BadgeLog
# 뱃지 레벨 리스트, 고객 뱃지 로그 확인, 관리자용 로그 출력 위한 파트

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'

class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)

    class Meta:
        model = UserBadge
        fields = ['id', 'user', 'badge', 'awarded_at']

class BadgeLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadgeLevel
        fields = '__all__'


class BadgeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadgeLog
        fields = '__all__'