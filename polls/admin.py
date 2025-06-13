from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    """Allows adding choices inline when editing a question."""
    model = Choice
    extra = 3  # Provides 3 empty choice fields by default

class QuestionAdmin(admin.ModelAdmin):
    """Customizes the admin panel for the Question model."""
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date Information", {"fields": ["pub_date"]}),
    ]
    inlines = [ChoiceInline]  # Displays choices inline within a question
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]  # Adds a search box for questions

# Register the models in Django admin
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
