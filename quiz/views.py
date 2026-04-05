from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Question
from .forms import AddQuestionForm, QuizAnswerForm
import random

def index(request):
    """Главная страница с выбором количества вопросов."""
 
    request.session.flush()
    return render(request, 'quiz/index.html')

def rules(request, limit):
    """Страница с правилами, сохраняем выбранный лимит."""
    request.session['quiz_limit'] = limit
    return render(request, 'quiz/rules.html', {'limit': limit})

def quiz(request):
    """Страница квиза: GET - первый вопрос, POST - проверка ответа."""
    questions = list(Question.objects.all())
    if not questions:
        messages.error(request, "Нет доступных вопросов. Добавьте хотя бы один.")
        return redirect('quiz:add_question')

    
    if request.method == 'GET':
        limit = request.session.get('quiz_limit', 5)
        max_questions = min(limit, len(questions))

        request.session['score'] = 0
        request.session['total'] = 0
        request.session['asked'] = []
        request.session['max_questions'] = max_questions

        
        remaining_indices = [i for i in range(len(questions)) if i not in request.session['asked']]
        if not remaining_indices:
            return redirect('quiz:result')
        current_index = random.choice(remaining_indices)
        request.session['current_question_index'] = current_index
        request.session['asked'].append(current_index)

        current_question = questions[current_index]
        form = QuizAnswerForm()
        return render(request, 'quiz/quiz.html', {
            'form': form,
            'question': current_question,
            'score': request.session['score'],
            'total': request.session['total'],
            'max_questions': max_questions,
        })


    if request.method == 'POST':
        form = QuizAnswerForm(request.POST)
        q_index = request.session.get('current_question_index')
        if q_index is None:
            messages.error(request, "Ошибка сессии. Начните игру заново.")
            return redirect('quiz:index')

        if form.is_valid():
            user_answer = form.cleaned_data['answer'].strip()
            current_question = questions[q_index]

            if user_answer.lower() == current_question.capital.lower():
                request.session['score'] += 1
                messages.success(request, f"✅ Верно! {current_question.country} – {current_question.capital}")
            else:
                messages.error(request, f"❌ Неверно. {current_question.country} – {current_question.capital}")

            request.session['total'] += 1

            
            if request.session['total'] >= request.session['max_questions'] or len(request.session['asked']) >= len(questions):
                return redirect('quiz:result')

           
            remaining_indices = [i for i in range(len(questions)) if i not in request.session['asked']]
            if not remaining_indices:
                return redirect('quiz:result')
            next_index = random.choice(remaining_indices)
            request.session['current_question_index'] = next_index
            request.session['asked'].append(next_index)
            next_question = questions[next_index]
            form = QuizAnswerForm()
            return render(request, 'quiz/quiz.html', {
                'form': form,
                'question': next_question,
                'score': request.session['score'],
                'total': request.session['total'],
                'max_questions': request.session['max_questions'],
            })
        else:
          
            current_question = questions[q_index]
            return render(request, 'quiz/quiz.html', {
                'form': form,
                'question': current_question,
                'score': request.session['score'],
                'total': request.session['total'],
                'max_questions': request.session['max_questions'],
            })

def result(request):
    """Страница результата."""
    score = request.session.get('score', 0)
    total = request.session.get('total', 0)
    
    quiz_limit = request.session.get('quiz_limit')
    request.session.flush()
    if quiz_limit:
        request.session['quiz_limit'] = quiz_limit
    return render(request, 'quiz/result.html', {'score': score, 'total': total})

def add_question(request):
    """Страница добавления нового вопроса."""
    if request.method == 'POST':
        form = AddQuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Вопрос '{form.cleaned_data['country']}' успешно добавлен!")
         
            form = AddQuestionForm()
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = AddQuestionForm()
    return render(request, 'quiz/add_question.html', {'form': form})