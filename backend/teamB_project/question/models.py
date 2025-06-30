from django.db import models
from main.models import User
from category.models import Category
# 실제 카테고리가 어디에 정의되는지에 따라 다름

# Create your models here.
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='question')
    # ranking 위한 필드 추가
    likes = models.ManyToManyField(User, related_name='liked_questions', blank=True)
    views = models.IntegerField(default=0)

    # 외래키

    title = models.CharField(max_length=500)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'question' # DB 테이블 명
        