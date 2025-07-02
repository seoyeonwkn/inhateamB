from django.db import models

class User(models.Model):
    login_id = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=100)  # 비번 해싱 안함. 테스트용
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.login_id

class Profile(models.Model):
    # profile_id는 django에서 자동으로 만들어주는 pk
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=30)
    job = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.user_name
    
class Portfolio(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profile}의 포트폴리오"