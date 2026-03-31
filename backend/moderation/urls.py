from django.urls import path, include
from rest_framework.routers import DefaultRouter

from moderation.views import *

router = DefaultRouter()

router.register('answer', AnswerModerationViewSet, basename='answer')
router.register('question', QuestionModerationViewSet, basename='question')

urlpatterns = [
    path('', include(router.urls), name='moderation'),
]
