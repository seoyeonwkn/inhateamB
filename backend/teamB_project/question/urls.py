from django.contrib import admin
from django.urls import path
# from .views import CategoryListCreateView, CategoryDetailView

# ranking
from .views import (
    QuestionRankingView,
    QuestionView,
    QuestionListView,
    BookmarkView
)

urlpatterns = [
    # 질문 관련
    path('questions/', QuestionView.as_view(), name='question-list-or-create'),                  # 전체 질문 조회(GET), 질문 생성(POST)
    path('questions/<int:pk>/', QuestionView.as_view(), name='question-detail-update-delete'),   # 특정 질문 조회, 수정, 삭제
    path('questions/search/', QuestionListView.as_view(), name='question-filtered-search'),      # 질문 조건 검색 (카테고리, 기간, 키워드 등)
    path('questions/rank/', QuestionRankingView.as_view(), name='question-ranking'),             # 질문 랭킹 조회 (조회수/좋아요/답변 수 기준)

    # 북마크 관련
    path('bookmarks/', BookmarkView.as_view(), name='bookmark-list'),                            # 북마크 조회 (GET), 삭제 (DELETE, 쿼리파라미터 포함)
    path('bookmarks/<int:question_id>/', BookmarkView.as_view(), name='bookmark-add'),           # 북마크 추가 (POST)
]