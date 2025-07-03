from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .utils import check_and_award_badges  # badge 앱 안에 있는 유틸함수
from main.models import User
from .models import Badge, UserBadge
from .serializers import BadgeSerializer, UserBadgeSerializer

from django.shortcuts import get_object_or_404



# 전체 뱃지 목록 조회 / 신규 뱃지 등록 (관리자 기능 포함)
class BadgeListCreateView(generics.ListCreateAPIView):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    # permission_classes = [IsAuthenticated]  # Postman: AllowAny로 완화
    permission_classes = [AllowAny]
"""
# 로그인한 사용자의 보유 뱃지 목록 조회
class UserBadgeListView(generics.ListAPIView):
    serializer_class = UserBadgeSerializer
    permission_classes = [IsAuthenticated]  # Postman: AllowAny로 완화

    def get_queryset(self):
        return UserBadge.objects.filter(user=self.request.user)
"""
# 뱃지 목록 조회 (token 없이 postman 확인용)

class UserBadgeListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        # user_id 유효 확인
        get_object_or_404(User, pk=user_id)

        # 해당 user_id의 뱃지 목록 조회
        badges = UserBadge.objects.filter(user_id=user_id)
        serializer = UserBadgeSerializer(badges, many=True)
        return Response(serializer.data)

"""    
# 사용자가 아직 획득하지 않은 뱃지 중 추천 (랜덤 3개)
class RecommendedBadgeView(APIView):
    permission_classes = [IsAuthenticated] # Postman: AllowAny로 완화

    def get(self, request):
        user = request.user

        # 현재 사용자가 보유한 뱃지 목록
        owned_ids = UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)

        # 아직 획득하지 않은 뱃지 중 추천 (현재는 상위 3개 고정)
        candidates = Badge.objects.exclude(id__in=owned_ids)[:3]

        serializer = BadgeSerializer(candidates, many=True)
        return Response(serializer.data)
    
"""
# 사용자가 아직 획득하지 않은 뱃지 중 추천 (랜덤 3개) (token 없이 postman 확인용)
class RecommendedBadgeView(APIView): 
    permission_classes = [AllowAny]   # 인증 없이도 조회 가능

    def get(self, request, user_id):
        # URL에서 받은 user_id로 User 조회
        user = get_object_or_404(User, id=user_id)

        # 현재 사용자가 보유한 뱃지 목록
        owned_ids = UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)

        # 아직 획득하지 않은 뱃지 중 추천 (현재는 상위 3개 고정)
        candidates = Badge.objects.exclude(id__in=owned_ids).order_by('level')[:3]

        serializer = BadgeSerializer(candidates, many=True)
        return Response(serializer.data)


"""
class AwardBadgeView(APIView):
    def post(self, request, user_id):
        # 해당 유저 가져오기
        user = get_object_or_404(User, id=user_id)
        # 뱃지 체크&지급 로직 실행
        check_and_award_badges(user)
        # 완료 응답
        return Response({'detail':'뱃지 지급 완료'}, status=status.HTTP_200_OK)
"""
# (token 없이 postman 확인용)
class AwardBadgeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, user_id):
        # 해당 유저 가져오기
        user = get_object_or_404(User, pk=user_id)

        # 바디에서 badge id 꺼내오기
        badge_id = request.data.get("badge")
        badge = get_object_or_404(Badge, pk=badge_id)

        # 3) 중복 지급 방지 (이미 있으면 400)
        if UserBadge.objects.filter(user=user, badge=badge).exists():
            return Response(
                {"detail": "이미 지급된 뱃지입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # UserBadge 생성
        user_badge = UserBadge.objects.create(
            user=user,
            badge=badge
        )

        # 5) 생성된 것을 직렬화해서 리턴해 주면 바로 확인 가능
        serializer = UserBadgeSerializer(user_badge)
        return Response(serializer.data, status=status.HTTP_201_CREATED)