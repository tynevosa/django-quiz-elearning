from django.contrib import admin

from authentication.models import StudentProfile

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
