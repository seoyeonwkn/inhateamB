from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Badge, UserBadge
from .serializers import BadgeSerializer, UserBadgeSerializer

# 전체 뱃지 목록 + 등록
class BadgeListCreateView(generics.ListCreateAPIView):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer

# 로그인한 사용자 뱃지 조회
class UserBadgeListView(generics.ListAPIView):
    serializer_class = UserBadgeSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny] # postman 확인 위해 임시로 자격 해제
    def get_queryset(self):
        return UserBadge.objects.filter(user=self.request.user)

# 추천 뱃지 보기
class RecommendedBadgeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        owned_ids = UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)
        candidates = Badge.objects.exclude(id__in=owned_ids)[:3]
        serializer = BadgeSerializer(candidates, many=True)
        return Response(serializer.data)
