from rest_framework import serializers

from game.models import Answer, Question
from django.utils.translation import gettext_lazy as _


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            "id",
            "text",
            "question"
        )
        read_only_fields = (
            "id",
        )


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            "id",
            "text"
        )
        read_only_fields = (
            "id",
        )


class AnswerQuestionSerializer(serializers.Serializer):
    text = serializers.CharField(help_text=_("Text to be used as a guess."))
