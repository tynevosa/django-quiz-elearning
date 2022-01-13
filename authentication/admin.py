from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from authentication.models import StudentProfile

from .models import User

# Register your models here.


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

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
