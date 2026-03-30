from django.contrib import admin

from game.models import Question, Answer, Session, SessionAnswer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('text',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text', 'is_active')
    list_filter = ('is_active', 'question',)
    search_fields = ('text',)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'finished_at')
    list_filter = ('user',)


@admin.register(SessionAnswer)
class SessionAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'answer', 'score', 'created_at',)
    list_filter = ('user', 'question', 'answer')

    @admin.display(description='User')
    def user(self, obj):
        return obj.user
