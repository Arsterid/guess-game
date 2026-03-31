from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.models import Session

from django.db import models
from user.models import User


class SessionObjectManager(models.Manager):
    def get_current_session_for_user(self, user: User) -> "Session":
        current_session = self.get_queryset().filter(user=user, finished_at=None).last()
        if current_session is None:
            current_session = self.create(user=user)
        return current_session
