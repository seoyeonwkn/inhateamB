from rest_framework import serializers
from .models import Badge, UserBadge, BadgeLevel, BadgeLog

# 뱃지 레벨 (ex: 고양이 전문가 → 고양이 박사)
class BadgeLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadgeLevel
        fields = ['level', 'title', 'condition_description']


# 뱃지 획득 이력 로그 (어떤 이유로 지급됐는지)
class BadgeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadgeLog
        fields = ['created_at', 'reason']


# 뱃지 기본 정보 (관리자 등록용, 프론트 표시용)
# 레벨 목록(levels)과, 획득 로그(logs)도 함께 노출
class BadgeSerializer(serializers.ModelSerializer):
    levels = BadgeLevelSerializer(many=True, read_only=True)
    logs = BadgeLogSerializer(source='userbadge__logs', many=True, read_only=True)

    class Meta:
        model = Badge
        fields = [
            'id', 'name', 'description',
            'level', 'condition_description', 'image_url',
            'previous_badge', 'category',
            'levels',     # 중첩된 BadgeLevel 정보
            'logs',       # 전체 뱃지 획득 reason 로그
        ]

class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)

    class Meta:
        model = UserBadge
        fields = ['id', 'user', 'badge', 'awarded_at']