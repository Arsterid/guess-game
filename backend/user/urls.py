from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from user.views import *

router = DefaultRouter()

router.register('user', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls), name='user'),
    path('user/auth/', obtain_auth_token, name='user-auth'),
]
