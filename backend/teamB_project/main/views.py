from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.shortcuts import get_object_or_404
from .models import User, Profile, Portfolio
from question.models import Question
from answer.models import Answer
from answer.serializers import AnswerSerializer
from .serializers import UserSerializer, ProfileSerializer, PortfolioSerializer

### User CRUD
class UserAPI(APIView):
    def get(self, request, user_id=None):
        if user_id:
            user = get_object_or_404(User, id=user_id)
            serializer = UserSerializer(user)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

### Profile CRUD
class ProfileAPI(APIView):
    def get(self, request, profile_id=None):
        if profile_id:
            profile = get_object_or_404(Profile, id=profile_id)
            serializer = ProfileSerializer(profile)
        else:
            profiles = Profile.objects.all()
            serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

### Portfolio CRUD
class PortfolioAPI(APIView):
    def get(self, request, portfolio_id=None):
        if portfolio_id:
            portfolio = get_object_or_404(Portfolio, id=portfolio_id)
            serializer = PortfolioSerializer(portfolio)
        else:
            portfolios = Portfolio.objects.all()
            serializer = PortfolioSerializer(portfolios, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PortfolioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, portfolio_id):
        portfolio = get_object_or_404(Portfolio, id=portfolio_id)
        serializer = PortfolioSerializer(portfolio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, portfolio_id):
        portfolio = get_object_or_404(Portfolio, id=portfolio_id)
        portfolio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 유저가 작성한 답변 목록 (정렬)
class UserAnswerListAPIView(APIView):
    def get(self, request, user_id):
        sort = request.GET.get('sort', 'latest')
        answers = Answer.objects.filter(user_id=user_id)

        if sort == 'likes':
            answers = answers.annotate(like_count=Count('likes')).order_by('-like_count')
        elif sort == 'accepted':
            answers = answers.order_by('-is_accepted', '-created_at')
        else:
            answers = answers.order_by('-created_at')

        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)

# 유저의 답변을 카테고리별로 정리
class UserAnswerByCategoryAPIView(APIView):
    def get(self, request, user_id):
        answers = Answer.objects.filter(user_id=user_id).select_related('question__category')
        category_dict = {}

        for answer in answers:
            category_name = answer.question.category.name
            if category_name not in category_dict:
                category_dict[category_name] = []
            category_dict[category_name].append(AnswerSerializer(answer).data)

        return Response(category_dict)

# 유저 통계 조회 (총 질문/답변/채택률)
class UserStatsAPIView(APIView):
    def get(self, request, user_id):
        total_questions = Question.objects.filter(user_id=user_id).count()
        total_answers = Answer.objects.filter(user_id=user_id).count()
        accepted_answers = Answer.objects.filter(user_id=user_id, is_accepted=True).count()

        stats = {
            "total_questions": total_questions,
            "total_answers": total_answers,
            "accepted_answers": accepted_answers,
            "acceptance_rate": f"{(accepted_answers / total_answers * 100):.1f}%" if total_answers else "0.0%",
        }
        return Response(stats)

# 인기 유저 랭킹
class PopularUserAPIView(APIView):
    def get(self, request):
        sort_by = request.GET.get('sort', 'answers')  # 기본은 답변 수

        if sort_by == 'likes':
            users = User.objects.annotate(
                total_likes=Count('answer__likes')
            ).order_by('-total_likes')
        else:
            users = User.objects.annotate(
                answer_count=Count('answer')
            ).order_by('-answer_count')

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)