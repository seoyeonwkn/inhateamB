from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User, Profile, Portfolio
from .serializers import UserSerializer, ProfileSerializer, PortfolioSerializer

### User CRUD
class UserAPI(APIView):
    def get(self, request, user_id=None):
        if user_id:
            user = get_object_or_404(User, id=user_id)
            serializer = UserSerializer(user)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

### Profile CRUD
class ProfileAPI(APIView):
    def get(self, request, profile_id=None):
        if profile_id:
            profile = get_object_or_404(Profile, id=profile_id)
            serializer = ProfileSerializer(profile)
        else:
            profiles = Profile.objects.all()
            serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

### Portfolio CRUD
class PortfolioAPI(APIView):
    def get(self, request, portfolio_id=None):
        if portfolio_id:
            portfolio = get_object_or_404(Portfolio, id=portfolio_id)
            serializer = PortfolioSerializer(portfolio)
        else:
            portfolios = Portfolio.objects.all()
            serializer = PortfolioSerializer(portfolios, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PortfolioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, portfolio_id):
        portfolio = get_object_or_404(Portfolio, id=portfolio_id)
        serializer = PortfolioSerializer(portfolio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, portfolio_id):
        portfolio = get_object_or_404(Portfolio, id=portfolio_id)
        portfolio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
