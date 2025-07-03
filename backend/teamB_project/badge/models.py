from django.db import models
from main.models import User
from category.models import Category 

class Badge(models.Model):
    """
    사용자에게 부여되는 뱃지 모델
    - 카테고리 기반 뱃지 업그레이드 구조
    """
    # 뱃지 이름
    name = models.CharField(max_length=100, unique=True)
    # 뱃지 설명    
    description = models.TextField()
    
    # 같은 카테고리 내의 뱃지 업그레이드
    level = models.IntegerField(default=1)
    
    # 획득 조건 설명
    condition_description = models.CharField(max_length=255)
    
    # 뱃지 이미지 URL
    image_url = models.URLField(null=True, blank=True)

    # 이전 단계의 뱃지
    previous_badge = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='upgraded_to'
    )

    # 뱃지 카테고리
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='badges'
    )

    def __str__(self):
        return f"[{self.category}] {self.name} (Lv.{self.level})" if self.category else f"{self.name} (Lv.{self.level})"



class UserBadge(models.Model):
    """
    사용자와 뱃지 간의 관계 (획득 내역)
    - 동일한 뱃지를 중복 획득하지 않도록 unique_together 설정
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='awarded_users')
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge')

    def __str__(self):
        return f"{self.user.login_id} - {self.badge.name}"

class BadgeLevel(models.Model):
    """
    뱃지의 세부 레벨 정의
    - 레벨별 명칭 및 조건
    """
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='levels')
    level = models.PositiveIntegerField()
    title = models.CharField(max_length=50)  # 예: 전문가, 박사, 신
    condition_description = models.CharField(max_length=255)

    class Meta:
        unique_together = ('badge', 'level')
        ordering = ['level']

    def __str__(self):
        return f"{self.badge.name} - {self.title}"


class BadgeLog(models.Model):
    """
    뱃지 지급 로그
    - 획득 이유 및 시점을 기록
    - 관리자 검토용
    """
    user_badge = models.ForeignKey(UserBadge, on_delete=models.CASCADE, related_name='logs')
    reason = models.CharField(max_length=200) # 뱃지 지급 이유
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_badge.user.login_id} → {self.reason}"
