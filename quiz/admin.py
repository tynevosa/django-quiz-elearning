from django.contrib import admin
from .models import Category, Question, Choice
from django.db import models
from quiz.forms import QuestionAdminForm
from quiz.widgets import AdminImageWidget
from django.utils.html import format_html


# Register your models here.
class ChoiceAdminInline(admin.TabularInline):
    model = Choice
    min_num = 1
    extra = 3
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
    }


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_filter = ('type', 'category', 'type', 'difficulty')
    list_display = ('body', 'image_tag', 'type', 'difficulty', 'category')
    search_fields = ('body',)
    form = QuestionAdminForm
    inlines = [ChoiceAdminInline]

    # Preview Image in change view
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
    }

    # Preview Image in List view
    def image_tag(self, obj):
        return format_html(f'<img src="{obj.image.url}" style="height:150px;width: auto" />') if obj.image and obj.image.url else None

    image_tag.short_description = 'Image'


class QuestionAdminInline(admin.StackedInline):
    model = Question
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [QuestionAdminInline]
