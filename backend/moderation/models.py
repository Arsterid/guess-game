from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from user.models import User


class ModerationResult(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object_id = models.BigIntegerField()
    content_object = GenericForeignKey('content_type', 'content_object_id')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user}: {self.result}'


class ModerationMixin(models.Model):
    on_moderation = models.BooleanField(default=True)
    is_moderated = models.BooleanField(default=False)

    class Meta:
        abstract = True
