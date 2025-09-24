from django.urls import path, include
from .views import BookList 
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='books_all')

urlpatterns = [
    path('book/', BookList.as_view(), name='books-list'),
    path('', include(router.urls)),
]