from django.urls import path
from .views import BadgeListCreateView, UserBadgeListView, RecommendedBadgeView

urlpatterns = [
    path('', BadgeListCreateView.as_view()),        # /api/badges/ |GET/POST: 전체 뱃지 목록 or 등록
    path('me/', UserBadgeListView.as_view()),       # /api/badges/me/ |GET: 내 뱃지 목록
    path('recommend/', RecommendedBadgeView.as_view()), # /api/badges/recommend/ |GET: 추천 뱃지 목록
    ]
