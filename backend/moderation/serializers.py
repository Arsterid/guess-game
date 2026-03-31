from rest_framework import serializers

from moderation.models import ModerationResult


class ModerationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModerationResult
        fields = (
            "id",
            "created_at",
            "content_type",
            "content_object_id",
            "result",
        )
        write_only_fields = (
            "result",
        )
        read_only_fields = (
            "id",
            "created_at",
            "content_type",
            "content_object_id",
        )
