import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db import connection
from django.db.models import Max
from django.db.models.query import Prefetch
from django.db.models.query_utils import FilteredRelation, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic.list import ListView

from quiz.forms import SubmitQuestionAnswer
from quiz.models import Category, Question, Score


# Create your views here.
def testmath(request):
    return render(request, 'testmath.html')


# Views
@login_required
def home(request):
    return render(request, "registration/success.html", {})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('quiz:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


from django.core import serializers


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "quiz/category_list.html"
    context_object_name = 'category_list'

    def get_queryset(self):
        return  Category.objects \
            .prefetch_related(Prefetch('score_category', queryset=Score.objects.filter(student=self.request.user), to_attr='student_score')) \
            .all()


class AnswerQuestionView(LoginRequiredMixin, View):

    def get(self, request, category_id):
        form = SubmitQuestionAnswer()

        category = get_object_or_404(Category, pk=category_id)

        try:
            student_score = Score.objects.get(student=request.user)
        except:
            student_score = Score.objects.create(category=category, student=request.user)
        finally:
            current_question = self.__get_student_next_question(category_id, request.user.id, student_score.value)
            self.__set_question_in_cache(category_id, request.user.id, current_question.pk)

            return render(request, 'quiz/answer_question.html', { 'question': current_question, 'form': form })

    def post(self, request, category_id):
        form = SubmitQuestionAnswer(request.POST)

        if not form.is_valid():
            return render(request, 'quiz/answer_question.html', {'form': form})

        answer = form.save(commit=False)

        # TODO:: handle multiple tabs
        student_score = Score.objects.get(student=request.user)
        current_question = self.__get_student_next_question(category_id, request.user.id, student_score)

        answer.is_correct = answer.student_answer == current_question.correct_answer
        answer.student = request.user
        answer.question = current_question
        answer.save()

        student_score.value = self.__evaluate_new_score(answer.is_correct, current_question.difficulty, student_score.value)
        student_score.save()

        self.__remove_question_form_cache(category_id, request.user.id)

        return redirect('quiz:answer_question', category_id=category_id)

    def __get_question_cache_key(self, category_id, student_id):
        return str(student_id) + '__' + str(category_id) + 'current_question'

    def __set_question_in_cache(self, category_id, student_id, question_id):
        cache_key = self.__get_question_cache_key(category_id, student_id)
        cache.set(cache_key, question_id)

    def __remove_question_form_cache(self, category_id, student_id):
        cache_key = self.__get_question_cache_key(category_id, student_id)
        cache.delete(cache_key)

    def __evaluate_new_score(self, is_correct, difficulty, score_value):
        if is_correct:
            score_value += difficulty
            score_value = min(score_value, 100)
        else :
            score_value -= difficulty
            score_value = max(score_value, 0)
        return score_value

    def __get_student_next_question(self, category_id, student_id, student_score, use_cache=True):
        cache_key = self.__get_question_cache_key(category_id, student_id)
        cached_question_id = cache.get(cache_key)

        if(use_cache and cached_question_id is not None): 
            return Question.objects.prefetch_related('choice_question').get(pk=cached_question_id)

        difficulty_level = student_score / 10

        query = Question.objects.prefetch_related('choice_question') \
            .annotate(answered=FilteredRelation('answer_question', condition=Q(answer_question__student=student_id,)),)

        # Unsolved questions based on difficulty
        current_question = query \
            .filter(category_id=category_id, answered__isnull=True, difficulty__gte=difficulty_level) \
            .order_by('difficulty') \
            .first()

        if(current_question is not None): return current_question

        # Get a random one of the already incorrectly solved ones
        randomSolvedQuestions = query \
            .annotate(final_attempt_is_correct=Max('answered__is_correct')) \
            .filter(Q(answered__isnull=False) | Q(answered__is_correct=False), category_id=category_id, final_attempt_is_correct__lt=1) \
            .values('id','body', 'category_id', 'correct_answer', 'difficulty', 'image', 'type', 'correct_answer', 'answered__student_id', 'answered__question_id', 'final_attempt_is_correct') \
            .order_by('difficulty') \
            .all()[:10]


        current_question = Question.objects.get(pk=random.choice(list(randomSolvedQuestions))['id'])

        return current_question
