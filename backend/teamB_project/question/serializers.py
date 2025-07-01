from rest_framework import serializers
from .models import Question, Bookmark
from category.serializers import CategorySerializer

class QuestionSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Question
        fields = '__all__' # 모든 속성을 직렬화
        read_only_fields = ['user', 'create_at', 'views', 'likes']

class BookmarkSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = ['id', 'question', 'created_at']