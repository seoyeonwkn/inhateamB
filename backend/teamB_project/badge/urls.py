from django.urls import path
from .views import BadgeListCreateView, UserBadgeListView

urlpatterns = [
    path('', BadgeListCreateView.as_view()),        # /api/badges/
    path('me/', UserBadgeListView.as_view()),       # /api/badges/me/
]
