from django.db import models
from main.models import User, Portfolio
from question.models import Question
# Create your models here.

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, related_name='answers')
    # 게시글이 삭제되었을때, 해당 게시글의 답글정보도 삭제할 것인지 정하기(답변으로 포트폴리오를 만들기 때문)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, null=True, blank=True, related_name='answers')
    # 포트폴리오가 삭제되더라도, 답변은 남겨야함

    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    likes = models.ManyToManyField(User, related_name='liked_answers', blank=True)

    def __str__(self):
        return f"Answer by {self.user.login_id} on Q{self.question.title}"
    
    def mark_as_accepted(self):
        Answer.objects.filter(question=self.question).update(is_accepted=False)
        # 한 게시글 당 하나의 답변만 채택될 수 있도록, 우선 모든 답변의 채택 여부를 False로 설정
        self.is_accepted = True
        self.save()
    
    class Meta:
        db_table = 'answer' # DB 테이블 이름

