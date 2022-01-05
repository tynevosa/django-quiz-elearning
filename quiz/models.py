from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})


class Question(models.Model):

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")

    class QuestionType(models.IntegerChoices):
        mcq = 1
        final_answer = 2

    DIFFICULTY_CHOICES = ((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'))

    # Fields
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to="questions", null=True, blank=True)
    difficulty = models.PositiveSmallIntegerField(choices=DIFFICULTY_CHOICES, default='5')
    correct_answer = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="topics")
    type = models.IntegerField(choices=QuestionType.choices, default=QuestionType.mcq)

    # Methods
    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return reverse("question_detail", kwargs={"pk": self.pk})



class Choice(models.Model):

    class Meta:
        verbose_name = _("choice")
        verbose_name_plural = _("choices")

    body = models.TextField(blank=True)
    image = models.ImageField(upload_to="choices", null=True, blank=True)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="topics"
    )

    def get_absolute_url(self):
        return reverse("choice_detail", kwargs={"pk": self.pk})
