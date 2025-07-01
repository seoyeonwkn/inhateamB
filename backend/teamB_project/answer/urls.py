from django.contrib import admin
from django.urls import path

from .views import (
    AcceptAnswerView,
    AnswerView,
    QuestionAnswersView,
    AnswerLikeView,
    AnswerAcceptedCheckView
)

urlpatterns = [
    path('answers/<int:answer_id>/accept/', AcceptAnswerView.as_view(), name='accept-answer'), # 답변 채택
    path('answers/', AnswerView.as_view(), name='answer-list-create'),                 # 전체 조회, 생성
    path('answers/<int:answer_id>/', AnswerView.as_view(), name='answer-detail'),      # 단일 조회, 수정, 삭제
    path('questions/<int:question_id>/answers/', QuestionAnswersView.as_view(), name='question-answers'), # 특정 게시물의 답변 조회 및 정렬
    path('answers/<int:answer_id>/like/', AnswerLikeView.as_view(), name='toggle-answer-like'), # 특정 답변에 좋아요 누르기
    path('answers/<int:answer_id>/is_accepted/', AnswerAcceptedCheckView.as_view(), name='answer-is-accepted'), # 특정 답변 채택 여부 확인
]