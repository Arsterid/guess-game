from django.conf import settings
from django.db import models
from django.db.models import Sum, Window, F, Value, IntegerField
from django.db.models.functions import Coalesce, RowNumber, Greatest
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import get_object_or_404

from game.managers import SessionObjectManager
from moderation.models import ModerationMixin
from user.models import User


class Question(
    ModerationMixin,
    models.Model
):
    text = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)

    def get_most_frequent_answers(self, limit: int = 5):
        return self.answers.order_by('-answer_quantity')[:limit]

    def get_answer_score(self, answer_id: int) -> int:
        qs = self.answers.annotate(
            position=Window(
                expression=RowNumber(),
                order_by=[F('answer_quantity').desc(), F('id').asc()]
            )
        ).annotate(
            answer_score=Greatest(
                Value(0),
                Value(settings.MAX_SCORE_PER_ANSWER) - (
                            (F('position') - 1) * (settings.MAX_SCORE_PER_ANSWER / settings.TOP_ANSWERS_LIMIT)),
                output_field=IntegerField()
            )
        )
        obj = get_object_or_404(qs, pk=answer_id)
        return obj.answer_score

    def __str__(self):
        return self.text[:50]


class Answer(
    ModerationMixin,
    models.Model
):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)

    answer_quantity = models.PositiveIntegerField(
        _("How many times this answer were given."),
        default=0
    )

    @property
    def score(self) -> int:
        return self.question.get_answer_score(self.id)

    def __str__(self):
        return f"{self.question_id}: {self.text[:50]}"


class Session(models.Model):
    objects = SessionObjectManager()

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def close(self):
        self.finished_at = timezone.now()
        self.save()

    @property
    def total_score(self) -> int:
        value = self.answers.aggregate(sum=Coalesce(Sum("score"), 0))["sum"]
        return value


class SessionAnswer(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='answers')

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True)
    score = models.PositiveIntegerField(_("Actual score of the answer."), default=0)

    created_at = models.DateTimeField(auto_now_add=True)
