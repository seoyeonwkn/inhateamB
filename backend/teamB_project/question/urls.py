from django.contrib import admin
from django.urls import path
# from .views import CategoryListCreateView, CategoryDetailView

# ranking
from .views import QuestionRankingView

urlpatterns = [
    path('ranking/', QuestionRankingView.as_view()),
]