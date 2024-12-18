from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import RandonneeViewSet, PointViewSet, PhotoViewSet
from .views import RandonneeViewSet, PointViewSet, PhotoViewSet, CustomAuthToken


router = DefaultRouter()
router.register(r'randonnees', RandonneeViewSet)
router.register(r'points', PointViewSet)
router.register(r'photos', PhotoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
