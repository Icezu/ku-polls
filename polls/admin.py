from django.contrib import admin

# Register your models here.
from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """Choice object config in Django admin page."""
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Question object config in Django admin page."""

    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Publish Date information', {'fields': ['pub_date'],
                                      'classes': ['collapse']}),
        ('End Date information', {'fields': ['end_date'],
                                  'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('id', 'question_text', 'pub_date',
                    'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
