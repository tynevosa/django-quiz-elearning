import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.cache import cache
from django.db.models.query_utils import FilteredRelation, Q
from django.shortcuts import redirect, render
from django.views import View

from quiz.forms import SubmitQuestionAnswer
from quiz.models import Question


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


class AnswerQuestionView(View):

    def get(self, request, category_id):
        form = SubmitQuestionAnswer()

        current_question = self.__get_student_next_question(category_id, request.user.id)
        self.__set_question_in_cache(category_id, request.user.id, current_question.pk)

        return render(request, 'quiz/answer_question.html', { 'question': current_question, 'form': form })

    def post(self, request, category_id):
        form = SubmitQuestionAnswer(request.POST)

        if not form.is_valid():
            return render(request, 'quiz/answer_question.html', {'form': form})

        answer = form.save(commit=False)

        # TODO:: handle multiple tabs
        current_question = self.__get_student_next_question(category_id, request.user.id)

        answer.is_correct = answer.student_answer == current_question.correct_answer
        answer.student = request.user
        answer.question = current_question
        answer.save()
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

    def __get_student_next_question(self, category_id, student_id, use_cache=True):
        cache_key = self.__get_question_cache_key(category_id, student_id)
        cached_question_id = cache.get(cache_key)

        if(use_cache and cached_question_id is not None): return Question.objects.get(pk=cached_question_id)

        query = Question.objects.annotate(answered=FilteredRelation('answer', condition=Q(answer__student__exact=student_id,)),)

        # Unsolved questions based on difficulty
        current_question = query \
            .filter(category_id__exact=category_id, answered__isnull=True,) \
            .order_by('difficulty') \
            .first()

        if(current_question is not None): return current_question

        # Get a random one of the already solved ones
        randomSolvedQuestions = query \
            .filter(category_id__exact=category_id, answered__isnull=False, answered__is_correct__exact=False) \
            .all()[:10]

        current_question = random.choice(list(randomSolvedQuestions))

        return current_question
