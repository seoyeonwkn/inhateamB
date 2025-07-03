from django.urls import path
from .views import BadgeListCreateView
from .views import UserBadgeListView
from .views import RecommendedBadgeView
from .views import AwardBadgeView
from .views import UserBadgeListView

urlpatterns = [
    path('',                  BadgeListCreateView.as_view()),         # [GET] 전체 뱃지 조회  [POST] 뱃지 생성
#    path('me/',               UserBadgeListView.as_view()),           # [GET] (임시) user-id 없이 자신의 뱃지 조회
#    path('recommend/',        RecommendedBadgeView.as_view()),        # [GET] 추천 뱃지 3개
    path('award/<int:user_id>/',  AwardBadgeView.as_view()),          # [POST] 토큰 없이 뱃지 지급
    path('recommend/<int:user_id>/', RecommendedBadgeView.as_view()), # [GET] 토큰 없이 추천 뱃지 3개
    path('user/<int:user_id>/',   UserBadgeListView.as_view()),       # [GET] 토큰 없이 특정 유저의 뱃지 조회
]


