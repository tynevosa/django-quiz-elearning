from django.db import models
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver
from django.urls import reverse
from django.utils.translation import gettext as _

from .helpers import RandomFileName


class MetaMethods():

    def __str__(self):
        return self.pk.__str__()

    def get_admin_url(self):
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.id,))

    def get_site_url(self):
        return reverse(f"{self._meta.model_name}_detail", kwargs={"pk": self.pk})


# Create your models here.
class Category(models.Model, MetaMethods):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(_("Show in Quiz?"), default=True)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name


class Question(models.Model, MetaMethods):

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
    difficulty = models.PositiveSmallIntegerField(choices=DIFFICULTY_CHOICES, default=5, db_index=True)
    correct_answer = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="%(class)s_category")
    type = models.IntegerField(choices=QuestionType.choices, default=QuestionType.mcq)


class Choice(models.Model, MetaMethods):

    class Meta:
        verbose_name = _("choice")
        verbose_name_plural = _("choices")

    body = models.TextField(blank=True)
    image = models.ImageField(upload_to=RandomFileName("choices"), null=True, blank=True)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="%(class)s_question"
    )


class Answer(models.Model, MetaMethods):

    class Meta:
        verbose_name = _("answer")
        verbose_name_plural = _("answers")

    # Fields
    user_answer = models.TextField(_("Answer"))
    user = models.ForeignKey("authentication.User", verbose_name=_("Student"), on_delete=models.CASCADE, related_name="%(class)s_answer")
    is_correct = models.BooleanField(_("Correct?"))
    question = models.ForeignKey(Question, verbose_name=_("Question"), on_delete=models.CASCADE, related_name="%(class)s_question")

    # Methods
    def __str__(self):
        return self.user_answer


class Score(models.Model, MetaMethods):

    class Meta:
        verbose_name = _("score")
        verbose_name_plural = _("scores")

    SCORE_CHOICES = zip(range(0, 100), range(0, 100))
    value = models.PositiveSmallIntegerField(choices=SCORE_CHOICES, default=0)

    category = models.ForeignKey(Category, verbose_name=_("Category"), on_delete=models.CASCADE, related_name="%(class)s_category")
    user = models.ForeignKey("authentication.User", verbose_name=_("Student"), on_delete=models.CASCADE, related_name="%(class)s_user")

    # Methods
    def __str__(self):
        return str(self.value)


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


# Auto disable categories with no questions
@receiver(pre_save, sender=Category)
def pre_save_category(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    try:
        test = Question.objects.filter(category=instance).all()[:1]
        if not test:
            instance.is_active = False
    except:
        pass
