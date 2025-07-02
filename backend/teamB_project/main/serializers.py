from rest_framework import serializers
from .models import User, Profile, Portfolio

# 유저 시리얼라이저
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'login_id', 'password', 'is_admin']

# 프로필 시리얼라이저
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'user_name', 'job', 'bio', 'image_url', 'updated_at']

# 포트폴리오 시리얼라이저
class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['id', 'profile']