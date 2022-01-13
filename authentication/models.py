# Create your models here.
from django.contrib.auth.models import (  # # A new class is imported. ##
    AbstractUser, BaseUserManager)
from django.db import models


class StudentProfile(models.Model):

    class Meta:
        app_label = 'quiz'

    class SchoolTypeChoices(models.TextChoices):
        national_arabic = 'NAT_AR', 'National Arabic'
        national_english = 'NAT_ENG', 'National English'
        american = 'US', 'American'
        ig = 'IG', 'IG'
        other = 'OTHER', 'Other'

    user = models.OneToOneField("authentication.User", on_delete=models.CASCADE, related_name="%(class)s_user")
    school = models.CharField(max_length=75, null=False, blank=False)
    school_type = models.CharField(max_length=30, choices=SchoolTypeChoices.choices, null=False, blank=False, default=SchoolTypeChoices.national_arabic)
    phone_number = models.CharField(max_length=75, null=False, blank=False)
    birth_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=75, null=False, blank=False)
    city = models.CharField(max_length=75, null=False, blank=False)
    how_did_you_hear_about_us = models.TextField(max_length=350, null=False, blank=False)

    def __str__(self):
        return self.user.first_name + self.user.last_name 


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
