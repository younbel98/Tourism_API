from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    language = models.CharField(
        max_length=5,
        choices=[("en", "English"), ("fr", "French"), ("ar", "Arabic")],
        default="en",
    )
    created_at = models.DateTimeField(auto_now_add=True)


class ConversationHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_site = models.CharField(max_length=255, null=True, blank=True)
    last_quiz_type = models.CharField(max_length=100, null=True, blank=True)
    last_intent = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


class VisitedSite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site_name = models.CharField(max_length=255)
    visited_at = models.DateTimeField(auto_now_add=True)


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site_type = models.CharField(max_length=100)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class BehaviorAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    behavior = models.CharField(max_length=100)
    site_name = models.CharField(max_length=255)
    triggered_at = models.DateTimeField(auto_now_add=True)


class Badge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge_id = models.CharField(max_length=100)
    awarded_at = models.DateTimeField(auto_now_add=True)
