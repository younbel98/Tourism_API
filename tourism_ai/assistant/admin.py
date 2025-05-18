from django.contrib import admin
from .models import (
    User,
    VisitedSite,
    QuizAttempt,
    BehaviorAlert,
    Badge,
    ConversationHistory,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "language", "created_at")
    search_fields = ("username",)


@admin.register(VisitedSite)
class VisitedSiteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "site_name", "visited_at")
    search_fields = ("site_name",)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "site_type", "score", "timestamp")
    list_filter = ("site_type",)


@admin.register(BehaviorAlert)
class BehaviorAlertAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "behavior", "site_name", "triggered_at")
    list_filter = ("behavior",)


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "badge_id", "awarded_at")
    list_filter = ("badge_id",)


@admin.register(ConversationHistory)
class ConversationHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "last_site",
        "last_quiz_type",
        "last_intent",
        "updated_at",
    )
