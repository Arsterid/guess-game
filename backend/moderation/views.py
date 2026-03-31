from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from game.models import Answer, Question
from game.serializers import AnswerSerializer, QuestionSerializer
from moderation.models import ModerationResult
from moderation.serializers import ModerationResultSerializer


class ModerationMixin:
    @action(methods=['POST'], detail=True, serializer_class=ModerationResultSerializer)
    def moderate(self, request, pk: int):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result: bool = serializer.validated_data["result"]

        obj = get_object_or_404(self.get_queryset(), pk=pk)
        obj.on_moderation = False
        obj.is_moderated = True if result else False
        obj.save()

        ModerationResult.objects.create(
            content_object=obj,
            result=result,
            user=self.request.user,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnswerModerationViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    ModerationMixin,
    GenericViewSet
):
    queryset = Answer.objects.filter(on_moderation=True)
    serializer_class = AnswerSerializer
    permission_classes = [IsAdminUser]


class QuestionModerationViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    ModerationMixin,
    GenericViewSet
):
    queryset = Question.objects.filter(on_moderation=True)
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminUser]
