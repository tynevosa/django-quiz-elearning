from django.db import models
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver
from django.urls import reverse
from django.utils.translation import gettext as _

from .helpers import RandomFileName


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

    DIFFICULTY_CHOICES = zip(range(1, 10), range(1, 10))

    # Fields
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to=RandomFileName("questions"), null=True, blank=True)
    difficulty = models.PositiveSmallIntegerField(choices=DIFFICULTY_CHOICES, default='5', db_index=True)
    correct_answer = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="question_category")
    type = models.IntegerField(choices=QuestionType.choices, default=QuestionType.mcq)

    # Methods
    def __str__(self):
        return self.pk.__str__()

    def get_admin_url(self):
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.id,))

    def get_site_url(self):
        return reverse("question_detail", kwargs={"pk": self.pk})


class Choice(models.Model):

    class Meta:
        verbose_name = _("choice")
        verbose_name_plural = _("choices")

    body = models.TextField(blank=True)
    image = models.ImageField(upload_to=RandomFileName("choices"), null=True, blank=True)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choice_question"
    )

    # def get_site_url(self):
    #     return reverse("choice_detail", kwargs={"pk": self.pk})


class Answer(models.Model):

    class Meta:
        verbose_name = _("answer")
        verbose_name_plural = _("answers")

    # Fields
    student_answer = models.TextField(_("Answer"))
    student = models.ForeignKey("auth.User", verbose_name=_("Student"), on_delete=models.CASCADE, related_name="answer_student")
    is_correct = models.BooleanField(_("Correct?"))
    question = models.ForeignKey(Question, verbose_name=_("Question"), on_delete=models.CASCADE, related_name="answer_question")

    # Methods
    def __str__(self):
        return self.student_answer

    def get_admin_url(self):
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.id,))

    def get_site_url(self):
        return reverse("answer_detail", kwargs={"pk": self.pk})


class Score(models.Model):

    class Meta:
        verbose_name = _("score")
        verbose_name_plural = _("scores")

    SCORE_CHOICES = zip(range(0, 100), range(0, 100))
    value = models.PositiveSmallIntegerField(choices=SCORE_CHOICES, default=0)

    category = models.ForeignKey(Category, verbose_name=_("Category"), on_delete=models.CASCADE, related_name="score_category")
    student = models.ForeignKey("auth.User", verbose_name=_("Student"), on_delete=models.CASCADE, related_name="score_student")

    # Methods
    def __str__(self):
        return self.value

    def get_admin_url(self):
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.id,))

    def get_site_url(self):
        return reverse("score_detail", kwargs={"pk": self.pk})


@receiver(pre_save, sender=Question)
def pre_save_question(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    try:
        old_image = instance.__class__.objects.get(id=instance.id).image.path
        try:
            new_image = instance.image.path
        except:
            new_image = None
        if new_image != old_image:
            import os
            if os.path.exists(old_image):
                os.remove(old_image)
    except:
        pass

