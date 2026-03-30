import random
from typing import Optional

from django.conf import settings
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from game.models import Answer, Question, Session, SessionAnswer
from game.serializers import AnswerSerializer, QuestionSerializer, AnswerQuestionSerializer


class AnswerViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    queryset = Answer.objects.filter(is_active=True, is_moderated=True)
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated,)


class QuestionViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet
                      ):
    queryset = Question.objects.filter(is_active=True, is_moderated=True)
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)

    @action(methods=['GET'], detail=False)
    def get_random_question(self, request):
        session = Session.objects.get_current_session_for_user(request.user)
        qs = self.get_queryset().exclude(
            id__in=session.answers.values_list("question_id", flat=True)
        )

        if not qs.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(instance=random.choice(qs))
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=True)
    def get_most_frequent_questions(self, request, pk: int):
        obj = get_object_or_404(Question, pk=pk)
        qs = obj.get_most_frequent_answers(settings.TOP_ANSWERS_LIMIT)

        serializer = AnswerSerializer(qs, many=True)
        return Response(serializer.data)

    @action(
        methods=["POST"],
        detail=True,
        serializer_class=AnswerQuestionSerializer
    )
    def guess_an_answer(self, request, pk: int):
        session = Session.objects.get_current_session_for_user(request.user)

        attempts = SessionAnswer.objects.filter(session=session, question=pk)
        if attempts.count() >= settings.ANSWER_ATTEMPT_LIMIT:
            raise ValidationError("You have no attempts left.")

        serializer = AnswerQuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        guess = serializer.validated_data["text"]

        obj: Question = get_object_or_404(Question, pk=pk)
        answer: Optional[Answer] = obj.answers.filter(text=guess).first()

        if answer is None:
            SessionAnswer.objects.create(
                user=request.user,
                session=session,
            )
            return Response("There is no such answer!", status=status.HTTP_204_NO_CONTENT)

        SessionAnswer.objects.create(
            user=request.user,
            session=session,
            answer=answer,
            score=answer.score
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class SessionViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated,)

    @action(methods=['GET'], detail=False)
    def get_total_score(self, request):
        current_session = Session.objects.get_current_session_for_user(request.user)
        return Response({"score": current_session.total_score}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def close_session(self, request):
        current_session = Session.objects.get_current_session_for_user(request.user)
        current_session.close()
        return Response(status=status.HTTP_200_OK)
