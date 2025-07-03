import random
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from .models import Badge, UserBadge
from main.models import User
from .serializers import BadgeSerializer, UserBadgeSerializer


# 전체 뱃지 목록 조회 / 새 뱃지 생성
class BadgeListCreateView(generics.ListCreateAPIView):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [AllowAny]


# 단일 뱃지 조회 / 수정 / 삭제
class BadgeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [AllowAny]


# 유저별 보유 뱃지 조회
class UserBadgeListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        get_object_or_404(User, pk=user_id)
        badges = UserBadge.objects.filter(user_id=user_id)
        serializer = UserBadgeSerializer(badges, many=True)
        return Response(serializer.data)


# 뱃지 지급 (토큰 없이 테스트용)
class AwardBadgeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        badge_id = request.data.get("badge")
        badge = get_object_or_404(Badge, pk=badge_id)

        if UserBadge.objects.filter(user=user, badge=badge).exists():
            return Response(
                {"detail": "이미 지급된 뱃지입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_badge = UserBadge.objects.create(user=user, badge=badge)
        serializer = UserBadgeSerializer(user_badge)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 사용자가 보유하지 않은 뱃지 중 랜덤 3개 추천
class RecommendedBadgeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)

        owned_ids = UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)
        unowned_badges = list(Badge.objects.exclude(id__in=owned_ids))
        recommended = random.sample(unowned_badges, min(len(unowned_badges), 3))

        serializer = BadgeSerializer(recommended, many=True)
        return Response(serializer.data)
