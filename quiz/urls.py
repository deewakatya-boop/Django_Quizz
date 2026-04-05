from django.urls import path
from . import views

app_name = 'quiz'  

urlpatterns = [
    path('', views.index, name='index'),
    path('rules/<int:limit>/', views.rules, name='rules'),
    path('quiz/', views.quiz, name='quiz'),
    path('result/', views.result, name='result'),    
    path('add/', views.add_question, name='add_question'),
]