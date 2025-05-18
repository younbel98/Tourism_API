from django.apps import AppConfig

from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def detect_intent(text):
    labels = ["qa", "quiz", "answer", "feedback"]
    result = classifier(text, candidate_labels=labels)
    return result["labels"][0]

class AssistantConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "assistant"
