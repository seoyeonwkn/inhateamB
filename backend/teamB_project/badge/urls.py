from django.urls import path
from .views import (
    BadgeListCreateView,
    BadgeDetailView,
    AwardBadgeView,
    UserBadgeListView,
    RecommendedBadgeView,
)

urlpatterns = [
    path('', BadgeListCreateView.as_view()),                   # [GET, POST] 전체 조회 / 생성
    path('<int:pk>/', BadgeDetailView.as_view()),              # [GET, PUT, DELETE] 상세 조회/수정/삭제
    path('award/<int:user_id>/', AwardBadgeView.as_view()),    # [POST] 뱃지 지급
    path('user/<int:user_id>/', UserBadgeListView.as_view()),  # [GET] 유저의 뱃지 목록
    path('recommend/<int:user_id>/', RecommendedBadgeView.as_view()),  # [GET] 미보유 랜덤 추천
]