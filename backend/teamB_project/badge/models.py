from django.db import models
from main.models import User
from category.models import Category 

class Badge(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    condition_description = models.CharField(max_length=255)
    image_url = models.URLField(null=True, blank=True)

    previous_badge = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='upgraded_to'
    )

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='badges'
    )

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='awarded_users')
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge')

    def __str__(self):
        return f"{self.user.login_id} - {self.badge.name}"

class BadgeLevel(models.Model):
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
    user_badge = models.ForeignKey(UserBadge, on_delete=models.CASCADE, related_name='logs')
    reason = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_badge.user.login_id} → {self.reason}"
