from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from .models import Question, Bookmark
from .serializers import QuestionSerializer, BookmarkSerializer
from django.shortcuts import get_object_or_404
from category.models import Category
from django.utils import timezone
from datetime import timedelta
from main.models import User

class QuestionView(APIView):
    def get(self, request, pk=None):
        if pk:  # 특정 질문 조회
            question = get_object_or_404(Question, pk=pk)
            serializer = QuestionSerializer(question)
            return Response(serializer.data)
        else: # 전체 질문 조회
            questions = Question.objects.all().order_by('-created_at')
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data)
    
    # 질문 생성
    def post(self, request):
        user_id = request.data.get('user')
        if not user_id:
            return Response({'detail': 'User의 ID가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
        except:
            return Response({'detail': '해당 유저가 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data.pop('user')
        
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            question = serializer.save(user=user) 
            return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED) # 질문 생성 성공
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 질문 생성 오류
    
    # 질문 수정
    def put(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        user_id = request.data.get('user_id')

        if not user_id or question.user.id != int(user_id): # 질문자와 요청자 다르면 수정 불가
            return Response({'detail': '수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 질문 삭제
    def delete(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        user_id = request.query_params.get('user_id')

        if not user_id or question.user.id != int(user_id):
            return Response({'detail': '삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) # 삭제 성공
        
class QuestionListView(APIView): # 질문 검색(카테고리별/제목 키워드별/기간 별/작성자 별)
    def get(self, request): 
        category_id = request.query_params.get('category')
        keyword = request.query_params.get('keyword')
        date_range = request.query_params.get('date') # '1', '7' , '30', '180'
        author_id = request.query_params.get('user')

        questions = Question.objects.all()

        if category_id: # 카테고리별 질문 조회(최신순)
            questions = questions.filter(category__id=category_id)
        
        if keyword: # 제목 키워드 별 조회
            questions = questions.filter(title__icontains=keyword)

        if date_range: # 기간 별 질문 조회
            valid_ranges = ['1', '7', '30', '180']
            if date_range not in valid_ranges:
                return Response(
                    {"detail": "날짜 필터는 1, 7, 30, 180 중 하나여야 합니다."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            days = int(date_range)
            since = timezone.now() - timedelta(days=days)
            questions = questions.filter(created_at__gte=since)

        if author_id: # 질문 작성자 기준 조회
            questions = questions.filter(user__id=author_id)
        
        questions = questions.order_by('-created_at') # 최신 순으로 정렬
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    

class QuestionRankingView(APIView): # 10위까지 랭킹(조회수, 좋아요 수, 답변 수)
    def get(self, request):
        sort = request.query_params.get('sort') 

        valid_sorts = ['likes', 'answers']
        if sort not in valid_sorts:
            return Response(
                {"detail": f"지원하지 않는 정렬 기준입니다. sort는 {valid_sorts} 중 하나여야 합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = Question.objects.annotate(
            answer_count=Count('answers', distinct=True),
            like_count=Count('likes', distinct=True)
        )

        if sort == 'likes':
            queryset = queryset.order_by('-like_count')
        elif sort == 'answers':
            queryset = queryset.order_by('-answer_count')

        top_questions = queryset[:10]
        serializer = QuestionSerializer(top_questions, many=True)
        return Response(serializer.data)
    
class BookmarkView(APIView):
    # 특정 User의 북마크 목록 조회
    def get(self, request):
        user_id = request.query_params.get('user')
        if not user_id:
            return Response({'detail': 'user 파라미터가 필요합니다.'},
            status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, pk=user_id)
        bookmarks = Bookmark.objects.filter(user=user).select_related('question')
        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data)
    
    # 특정 User의 북마크 추가
    def post(self, request, question_id):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'detail': 'user_id가 필요합니다.'},
            status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, pk=user_id)
        question = get_object_or_404(Question, pk=question_id)

        bookmark, created = Bookmark.objects.get_or_create(user=user, question=question)

        if not created:
            return Response({'detail': '이미 북마크한 질문입니다.'},
            status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BookmarkSerializer(bookmark)
        return Response(serializer.data ,status=status.HTTP_201_CREATED)
    
    def delete(self, request, question_id):
        user_id = request.query_params.get('user')
        if not user_id:
            return Response({'detail': 'user 파라미터가 필요합니다.'},
            status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, pk=user_id)
        question = get_object_or_404(Question, pk=question_id)

        bookmark = Bookmark.objects.filter(user=user, question=question).first()

        if not bookmark:
            return Response({'detail': '북마크하지 않은 질문입니다.'},
            status=status.HTTP_404_NOT_FOUND)
        
        bookmark.delete()
        return Response("북마크가 삭제되었습니다.", status=status.HTTP_204_NO_CONTENT)

# 토글 형식 질문 좋아요 기능
class QuestionLikeView(APIView):
    # 좋아요 추가 또는 취소
    def post(self, request, question_id):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'detail': 'user_id가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, pk=user_id)
        question = get_object_or_404(Question, pk=question_id)

        if user in question.likes.all():
            question.likes.remove(user)
            return Response({'detail': '좋아요가 취소되었습니다.'}, status=status.HTTP_200_OK)
        else:
            question.likes.add(user)
            return Response({'detail': '좋아요가 추가되었습니다.'}, status=status.HTTP_201_CREATED)
    
    # 특정 질문의 좋아요 누적 수 조회
    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        like_count = question.likes.count()
        return Response({
            'question_id': question.id,
            'like_count': like_count
        }, status=status.HTTP_200_OK)
        

    
