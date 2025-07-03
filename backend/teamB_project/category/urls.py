from django.urls import path
from .views import CategoryListCreateView, CategoryDetailView

urlpatterns = [
    path('', CategoryListCreateView.as_view()),
    # GET /api/categories/
    path('<int:pk>/', CategoryDetailView.as_view()),
    # GET/PUT/DELETE /api/categories/3/
]
