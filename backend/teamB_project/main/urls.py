from django.urls import path
from .views import UserAPI, ProfileAPI, PortfolioAPI

urlpatterns = [
    path('users/', UserAPI.as_view()),
    path('users/<int:user_id>/', UserAPI.as_view()),

    path('profiles/', ProfileAPI.as_view()),
    path('profiles/<int:profile_id>/', ProfileAPI.as_view()),

    path('portfolios/', PortfolioAPI.as_view()),
    path('portfolios/<int:portfolio_id>/', PortfolioAPI.as_view()),
]
