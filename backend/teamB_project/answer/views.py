from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Answer, AnswerReport
from .serializers import AnswerSerializer, AnswerReportSerializer
from django.shortcuts import get_object_or_404
from main.models import User
from question.models import Question
from django.db.models import Count

class AcceptAnswerView(APIView):  # 답변 채택
    def post(self, request, answer_id):
        user_id = request.data.get('user_id') # 답변을 채택하는 사람
        if not user_id:
            return Response({'detail': 'user_id가 필요합니다.'},
            status=status.HTTP_400_BAD_REQUEST)
        
        answer = get_object_or_404(Answer, pk=answer_id) # 채택할 답변
        question = answer.question

        if not question: # 답변이 달린 질문이 삭제된 경우
            return Response({'detail': '이 답변은 삭제된 질문에 달려 있어 채택할 수 없습니다.'},
                status=status.HTTP_400_BAD_REQUEST)
        if question.user.id != int(user_id):
            return Response({'detail': '채택 권한이 없습니다. 질문 작성자만 채택할 수 있습니다.'},
                    status=status.HTTP_403_FORBIDDEN)
        
        answer.mark_as_accepted()
        return Response({'detail': '답변이 채택되었습니다.'}, status=status.HTTP_200_OK)
    

class AnswerView(APIView):
    # 전체 답변 조회 또는 특정 답변 조회
    def get(self, request, answer_id=None):
        if answer_id:
            answer = get_object_or_404(Answer, pk=answer_id)
            serializer = AnswerSerializer(answer)
            return Response(serializer.data)
        else:
            answers = Answer.objects.all()
            serializer = AnswerSerializer(answers, many=True)
            return Response(serializer.data)

    # 답변 등록
    def post(self, request):
        user_id = request.data.get('user_id')
        question_id = request.data.get('question_id')
        body = request.data.get('body')

        if not (user_id and question_id and body):
            return Response({'detail': 'user_id, question_id, body는 필수입니다.'},
            status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, pk=user_id)
        question = get_object_or_404(Question, pk=question_id)

        answer = Answer.objects.create(user=user, question=question, body=body)
        serializer = AnswerSerializer(answer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # 답변 수정 (작성자만)
    def put(self, request, answer_id):
        answer = get_object_or_404(Answer, pk=answer_id)
        user_id = request.data.get('user_id')

        if not user_id or answer.user.id != int(user_id):
            return Response({'detail': '수정 권한이 없습니다.'},
            status=status.HTTP_403_FORBIDDEN)
        
        body = request.data.get('body')
        if not body:
            return Response({'detail': 'body 값이 필요합니다.'}, 
            status=status.HTTP_400_BAD_REQUEST)

        answer.body = body
        answer.save()
        serializer = AnswerSerializer(answer)
        return Response(serializer.data)

    # 답변 삭제 (작성자만)
    def delete(self, request, answer_id):
        answer = get_object_or_404(Answer, pk=answer_id)
        user_id = request.query_params.get('user_id')

        if not user_id or answer.user.id != int(user_id):
            return Response({'detail': '삭제 권한이 없습니다.'},
            status=status.HTTP_403_FORBIDDEN)
        
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class QuestionAnswersView(APIView): # 특정 게시물의 답변 조회 및 정렬하기
    def get(self, request, question_id):
        sort = request.query_params.get('sort', 'recent')

        question = get_object_or_404(Question, pk=question_id)
        answers = Answer.objects.filter(question=question)

        if sort == 'likes': # 좋아요 순
            answers = answers.annotate(like_count=Count('likes')).order_by('-is_accepted', '-like-count', '-created_at')
        
        else: # 최신 순 또는 잘못된 값
            answers = answers.order_by('-is_accepted', '-created_at')
        
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)

class AnswerLikeView(APIView): # 좋아요 및 좋아요 취소(토글 형식)
    def post(self, request, answer_id):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'detail': 'user_id가 필요합니다.'},
                status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, pk=user_id)
        answer = get_object_or_404(Answer, pk=answer_id)

        if user in answer.likes.all(): # 해당 답변의 좋아요 목록에 user가 있는 경우
            answer.likes.remove(user)
            return Response({'detail': '좋아요가 취소되었습니다.'}, 
                status=status.HTTP_200_OK)
        else: # 해당 답변의 좋아요 목록에 user가 없는 경우
            answer.likes.add(user)
            return Response({'detail': '좋아요가 추가되었습니다.'},
                status=status.HTTP_201_CREATED)

class AnswerAcceptedCheckView(APIView): # 특정 답변 채택 여부 확인
    def get(self, request, answer_id):
        answer = get_object_or_404(Answer, pk=answer_id)

        return Response({
            'answer_id': answer.id,
            'is_accepted': answer.is_accepted
        }, status=status.HTTP_200_OK)

class AnswerReportView(APIView): 
    # 특정 답변에 대한 누적 신고 수 조회
    def get(self, request, answer_id):
        answer = get_object_or_404(Answer, pk=answer_id)
        report_count = AnswerReport.objects.filter(answer=answer).count()
        return Response({
            'answer_id': answer.id,
            'report_count': report_count
        }, status=status.HTTP_200_OK)
    
    # 특정 답변 신고하기
    def post(self, request): 
        user_id = request.data.get('user_id')
        answer_id = request.data.get('answer_id')
        reason = request.data.get('reason')

        if not all([user_id, answer_id, reason]):
            return Response({'detail': 'user_id, answer_id, reason이 모두 필요합니다.'},
                status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, pk=user_id)
        answer = get_object_or_404(Answer, pk=answer_id)

        # 동일 user의 중복 신고 방지
        if AnswerReport.objects.filter(user=user, answer=answer).exists():
            return Response({'detail': '이미 신고한 답변입니다.'},
                status=status.HTTP_400_BAD_REQUEST)
        
        report = AnswerReport.objects.create(user=user, answer=answer, reason=reason)
        serializer = AnswerReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    