from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class StudentProfile(models.Model):
    class Meta:
        app_label = 'quiz'

    class SchoolTypeChoices(models.TextChoices):
        national_arabic = 'NAT_AR', 'National Arabic'
        national_english = 'NAT_ENG', 'National English'
        american = 'US', 'American'
        ig = 'IG', 'IG'
        other = 'OTHER', 'Other'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="%(class)s_user")
    school = models.CharField(max_length=75, null=False, blank=False)
    school_type = models.CharField(max_length=30, choices=SchoolTypeChoices.choices,null=False, blank=False, default=SchoolTypeChoices.national_arabic)
    phone_number = models.CharField(max_length=75, null=False, blank=False)
    birth_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=75, null=False, blank=False)
    city = models.CharField(max_length=75, null=False, blank=False)
    how_did_you_hear_about_us = models.TextField(max_length=350, null=False, blank=False)

    def __str__(self):
        return self.user.first_name + self.user.last_name 
