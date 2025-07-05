from rest_framework import serializers
from .models import Question, Bookmark
from category.serializers import CategorySerializer
from main.serializers import UserSerializer

class QuestionSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    categories = CategorySerializer(read_only=True, many=True)    
    like_count = serializers.SerializerMethodField()
    answer_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Question
        fields = '__all__' # 모든 속성을 직렬화
        read_only_fields = ['created_at', 'views', 'likes']
    
    def get_like_count(self, obj):
        return obj.likes.count()
    
    def get_user(self, obj): # anony가 True일때, 익명으로 보이기

        if obj.anony:
            return {'login_id': '익명'}
        return UserSerializer(obj.user).data

class BookmarkSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = ['id', 'question', 'created_at']