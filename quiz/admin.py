from django.contrib import admin
from django.db import models
from django.utils.html import format_html

from quiz.forms import QuestionAdminForm
from quiz.models import Answer, Score, StudentProfile
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
    list_display = ['name', 'is_active']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'question_body_image', 'user_answer', 'is_correct']
    list_filter = ('user', 'question', 'is_correct')

    def get_fieldsets(self, request, obj=None):
        fs = super(AnswerAdmin, self).get_fieldsets(request, obj)
        fs[0][1]['fields'] = list((field for field in fs[0][1]['fields'] if field != 'question'))
        return fs

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields] + ['question_body_image']

    def question_body_image(self, obj):
        return format_html(f'<span class="renderedMathJax">{obj.question.body}<span/>' +
        f'<span><img src="{obj.question.image.url}" style="height:150px;width: auto" /><span/>' if obj.question.image and obj.question.image.url else None)

    question_body_image.short_description = 'Question'


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_filter = ('school',)
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    list_display = ['student_name', 'email', 'school', 'country', 'phone_number', 'city', 'birth_date', 'school_type']
    readonly_fields = ['student_name', 'how_did_you_hear_about_us', ]
    exclude = ['user']

    def student_name(self, obj):
        return obj.user.first_name + obj.user.last_name

    student_name.short_description = 'Name'

    def email(self, obj):
        return obj.user.email

    # Disable adding ones from dashboard
    def has_add_permission(self, request):
        return False


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    # Disable adding ones from dashboard
    list_display = ['student_name', 'category', 'total_score', ]
    readonly_fields = ['user', 'category']

    def total_score(self, obj):
        return obj.value

    def student_name(self, obj):
        return obj.user.first_name + obj.user.last_name

    def has_add_permission(self, request):
        return False
