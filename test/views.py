# test/views.py
from django.shortcuts import render, redirect
from .models import Question
from .forms import TestForm


def test_view(request):
    questions = Question.objects.all()

    if request.method == 'POST':
        form = TestForm(request.POST, questions=questions)
        if form.is_valid():
            # Подсчет правильных ответов
            score = 0
            for question in questions:
                selected_choice = int(form.cleaned_data[f'question_{question.id}'])
                if question.choices.get(id=selected_choice).is_correct:
                    score += 1

            # Отображаем результат
            return render(request, 'test/test_result.html', {'score': score, 'total': len(questions)})
    else:
        form = TestForm(questions=questions)

    return render(request, 'test/test.html', {'form': form, 'active_page': 'test'})
