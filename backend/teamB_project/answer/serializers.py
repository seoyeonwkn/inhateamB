from rest_framework import serializers
from .models import Answer
from main.models import User
from question.models import Question

class AnswerSerializer(serializers.ModelSerializer):
    user_login_id = serializers.CharField(source='user.login_id', read_only=True)
    question_title = serializers.CharField(source='question.title', read_only=True)
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = [
            'id',
            'user_login_id',
            'question_title',
            'body',
            'created_at',
            'is_accepted',
            'like_count',
        ]
    
    def get_like_count(self, obj):
        return obj.likes.count()