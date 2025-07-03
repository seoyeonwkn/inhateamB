"""
URL configuration for teamB_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.urls import re_path

from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg       import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="B team 해커톤 project",
        default_version='프로젝트 버전: ?',
        description="B team 해커톤 project API 문서",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="likelion@inha.edu"), 
        license=openapi.License(name="backend"),     
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('main.urls')),
    path('question/', include('question.urls')),
    path('answer/', include('answer.urls')),
    path('api/categories/', include('category.urls')),
    path('api/badges/', include('badge.urls')),
<<<<<<< HEAD
=======

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
>>>>>>> 78e884844e654d9f5b8f19e3ff38d49f7e43803e
]