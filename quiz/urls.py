from django.urls import path

from . import views

app_name = 'quiz'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:category_id>/answer-question', views.AnswerQuestionView.as_view(), name='answer_question'),
]
