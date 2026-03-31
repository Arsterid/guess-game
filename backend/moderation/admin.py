from django.contrib import admin

from moderation.models import ModerationResult


@admin.register(ModerationResult)
class ModerationResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content_object', 'result', 'created_at')
    list_filter = ('user', 'result',)

