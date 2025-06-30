from rest_framework import generics
from .models import Badge, UserBadge
from .serializers import BadgeSerializer, UserBadgeSerializer
from rest_framework.permissions import IsAuthenticated

# 전체 뱃지 목록 + 등록
class BadgeListCreateView(generics.ListCreateAPIView):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer

# 로그인한 사용자 뱃지 조회
class UserBadgeListView(generics.ListAPIView):
    serializer_class = UserBadgeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserBadge.objects.filter(user=self.request.user)

