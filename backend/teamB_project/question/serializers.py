from rest_framework import serializers
from .models import Question, Bookmark
from category.serializers import CategorySerializer

class QuestionSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = '__all__' # 모든 속성을 직렬화
        read_only_fields = ['user', 'created_at', 'views', 'likes']
    
    def get_like_count(self, obj):
        return obj.likes.count()

class BookmarkSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = ['id', 'question', 'created_at']