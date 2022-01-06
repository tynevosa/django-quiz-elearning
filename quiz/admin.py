from django.contrib import admin
from django.db import models
from django.urls.base import reverse
from django.utils.html import format_html

from quiz.forms import QuestionAdminForm
from quiz.widgets import AdminImageWidget

from .models import Category, Choice, Question


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
    search_fields = ('body',)
    list_filter = ('type', 'category', 'difficulty')
    list_display = ('body', 'image_tag', 'type', 'difficulty', 'category', 'action_tag')
    readonly_fields = ('renderedBody',)
    list_per_page = 10
    form = QuestionAdminForm
    inlines = [ChoiceAdminInline]

    # Preview Image in change view
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
    }

    # Move body & renderedBody to the beggining of the fieldset
    def get_fieldsets(self, request, obj=None):
        fs = super(QuestionAdmin, self).get_fieldsets(request, obj)
        fs[0][1]['fields'] = ['body', 'renderedBody'] + list((field for field in fs[0][1]['fields'] if field != 'body' and field != 'renderedBody'))
        return fs

    def renderedBody(self, obj):
        return format_html(f'<span class="renderedMathJax">{obj.body}<span/>')

    renderedBody.short_description = 'Preview'

    # Preview Image in List view
    def image_tag(self, obj):
        return format_html(f'<img src="{obj.image.url}" style="height:150px;width: auto" />') if obj.image and obj.image.url else None

    image_tag.short_description = 'Image'

    def action_tag(self, obj):
        return format_html(f'<a href="{obj.get_admin_url()}" title="View"> <i class="fas fa-eye fa-sm"></i> </a>')

    action_tag.short_description = ''


class QuestionAdminInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [QuestionAdminInline]
