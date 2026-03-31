from rest_framework import serializers

from game.models import Answer, Question
from django.utils.translation import gettext_lazy as _


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            "id",
            "text",
            "question",
            "answer_quantity",
        )
        read_only_fields = (
            "id",
            "answer_quantity",
        )
        extra_kwargs = {
            'text': {'validators': []},
        }

    def create(self, validated_data):
        if obj := Answer.objects.filter(text=validated_data["text"]).first():
            obj.answer_quantity += 1
            obj.save()
            return obj

        return super().create(validated_data)


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
