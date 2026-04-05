import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from quiz.models import Question

def load_questions():
    with open('questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)

    count = 0
    for q in questions:
        obj, created = Question.objects.get_or_create(
            country=q['country'],
            defaults={
                'country_genitive': q['country_genitive'],
                'capital': q['capital']
            }
        )
        if created:
            count += 1
            print(f"Добавлен: {q['country']} — {q['capital']}")
        else:
            print(f"Уже есть: {q['country']}")

    print(f"\nВсего добавлено новых вопросов: {count}")

if __name__ == '__main__':
    load_questions()