from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from .models import Question
from .serializers import QuestionSerializer

class QuestionRankingView(APIView): # 10위까지 랭킹(조회수, 좋아요 수, 답변 수)
    def get(self, request):
        sort = request.query_params.get('sort', 'views')  # 기본은 조회수 ranking

        valid_sorts = ['likes', 'answers', 'views']
        if sort not in valid_sorts:
            return Response(
                {"detail": f"지원하지 않는 정렬 기준입니다. sort는 {valid_sorts} 중 하나여야 합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = Question.objects.annotate(
            answer_count=Count('answer'),
            like_count=Count('likes')
        )

        if sort == 'likes':
            queryset = queryset.order_by('-like_count')
        elif sort == 'answers':
            queryset = queryset.order_by('-answer_count')
        else:  # 'views'
            queryset = queryset.order_by('-views')

        top_questions = queryset[:10]
        serializer = QuestionSerializer(top_questions, many=True)
        return Response(serializer.data)