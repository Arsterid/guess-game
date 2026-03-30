from django.urls import path, include
from rest_framework.routers import DefaultRouter

from game.views import *

router = DefaultRouter()

router.register('answer', AnswerViewSet, basename='answer')
router.register('question', QuestionViewSet, basename='question')

urlpatterns = [
    path('', include(router.urls), name='game'),
]
