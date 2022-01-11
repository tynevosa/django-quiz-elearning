import random

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.core.cache import cache
from django.db.models import Max
from django.db.models.query import Prefetch
from django.db.models.query_utils import FilteredRelation, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic.list import ListView

from quiz.forms import StudentProfileForm, SubmitQuestionAnswer
from quiz.models import Category, Question, Score


# Create your views here.
def testmath(request):
    return render(request, 'testmath.html')


# Views
@login_required
def home(request):
    return redirect('quiz:category_list')


def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        student_profile_form = StudentProfileForm(request.POST)

        if user_form.is_valid() and student_profile_form.is_valid():
            user = user_form.save()
            student_profile = student_profile_form.save(commit=False)
            student_profile.user = user
            student_profile.save()

            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('quiz:category_list')

    else:
        user_form = UserCreationForm()
        student_profile_form = StudentProfileForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'student_profile_form': student_profile_form})


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "quiz/category_list.html"
    context_object_name = 'category_list'

    def get_queryset(self):
        return  Category.objects \
            .prefetch_related(Prefetch('score_category', queryset=Score.objects.filter(user=self.request.user), to_attr='user_score')) \
            .filter(is_active=True) \
            .all()


class AnswerQuestionView(LoginRequiredMixin, View):

    def get(self, request, category_id):
        form = SubmitQuestionAnswer()

        category = get_object_or_404(Category, pk=category_id)

        try:
            student_score = Score.objects.get(user=request.user)
        except:
            student_score = Score.objects.create(category=category, user=request.user)

        try:
            current_question = self.__get_student_next_question(category_id, request.user.id, student_score.value)
            self.__set_question_in_cache(category_id, request.user.id, current_question.pk)

            return render(request, 'quiz/answer_question.html', { 'question': current_question, 'form': form })
        except:
            return redirect('quiz:category_list')

    def post(self, request, category_id):
        form = SubmitQuestionAnswer(request.POST)

        if not form.is_valid():
            return render(request, 'quiz/answer_question.html', {'form': form})

        answer = form.save(commit=False)

        student_score = Score.objects.get(user=request.user)
        current_question = self.__get_student_next_question(category_id, request.user.id, student_score)

        answer.is_correct = answer.user_answer == current_question.correct_answer
        answer.user = request.user
        answer.question = current_question
        # TODO:: handle multiple tabs
        # try:
        #     already_solved = Answer.objects.get(student=request.user, is_correct=True, question=answer.question)
        #     if(already_solved is not None):
        #         messages.error(request, 'This question was already solved')

        #         return redirect('quiz:answer_question', category_id=category_id)
        # except:
            # Did not solve correctly before
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
            .annotate(answered=FilteredRelation('answer_question', condition=Q(answer_question__user=student_id,)),)

        # Unsolved questions based on difficulty
        current_question = query \
            .filter(category_id=category_id, answered__isnull=True, difficulty__gte=difficulty_level) \
            .order_by('difficulty') \
            .first()

        if(current_question is not None): return current_question

        # Get a random one of the already incorrectly solved ones
        randomSolvedQuestions = query \
            .annotate(final_attempt_is_correct=Max('answered__is_correct')) \
            .filter(Q(answered__isnull=False) | Q(answered__is_correct=False), category_id=category_id, final_attempt_is_correct=False) \
            .values('id', 'body', 'category_id', 'correct_answer', 'difficulty', 'image', 'type', 'correct_answer', 'answered__user_id', 'answered__question_id', 'final_attempt_is_correct') \
            .order_by('difficulty') \
            .all()[:10]

        current_question = Question.objects.get(pk=random.choice(list(randomSolvedQuestions))['id'])

        return current_question
