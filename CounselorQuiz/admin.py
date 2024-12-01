from django.contrib import admin
from .models import QuizQuestion, QuizOption
# Register your models here.

class ChoiceInLine(admin.TabularInline):
    model = QuizOption

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLine]          # displaying the choice model together with question
    search_fields = ['question_text']     # adds a search bar for the question_text field
    list_display="counselor","question_text"

admin.site.register(QuizQuestion, QuestionAdmin)
