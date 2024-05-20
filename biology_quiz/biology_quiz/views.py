from django.core.cache import cache
from django.shortcuts import render

from . import quiz_work as qw


def index(request):
    context = {
        "quizzes": qw.get_quizzes(),
        "user_stats": qw.get_users_stats()
    }
    return render(request, "index.html", context=context)


def play_quiz(request, id):
    quiz, questions = qw.get_quiz(id)
    context = {
        "quiz": quiz,
        "questions": questions
    }
    return render(request, 'play_quiz.html', context=context)


def validate_quiz(request, id):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("username")
        email = request.POST.get("email")
        answers = {}
        for i, v in request.POST.items():
            if 'answer' in i:
                i = i.replace('answer_', '')
                answers[i] = v

        correct_answers, percent = qw.make_result(user_name, email, answers)
        context = {
            "user": user_name,
            "result": correct_answers,
            "percent": percent
        }
        return render(request, 'quiz_game_result.html', context=context)
    else:
        return play_quiz(request, id)


def add_quiz(request):
    return render(request, 'add_quiz.html',
                  context={'question_count': range(2)})


def save_quiz(request):
    questions = {}
    answers = {}
    name = None
    description = None
    for key, value in request.POST.items():
        if 'quizName' == key:
            name = value
        if 'quizDescription' == key:
            description = value
        if "question_" in key:
            question_id = key.split(sep='_')[1]
            if question_id not in questions:
                questions[question_id] = value

        if "answer_" in key:
            question_id, answer_id = key.split(sep='_')[1:]
            if question_id not in answers:
                answers[question_id] = {}
            answers[question_id][answer_id] = value

        if 'correct_' in key:
            question_id = key.split(sep='_')[1]
            answers[question_id]['correct_answer'] = answers[question_id][value]

    image = request.FILES.get('image')

    context = {'success': True, "comment": "Викторина сохранена"}

    if not name:
        context['success'] = False
        context['comment'] = "Не задано имя викторины!"
    if not description:
        context['success'] = False
        context['comment'] = "Не задано описание викторины!"
    for i in questions.values():
        if not i:
            context['success'] = False
            context['comment'] = "Не заполены все вопросы!"
    for key, val in answers.items():
        if len(val) < 4:
            context['success'] = False
            context['comment'] = "Не заполнены все варианты ответов!"
        for i in val.values():
            if not i:
                context['success'] = False
                context['comment'] = "Не заполнены все варианты ответов!"
    if image:
        if 'jpg' not in image.content_type and 'png' not in image.content_type:
            context['success'] = False
            context['comment'] = "Неверный формат изображения! Доступны jpg и png"

    if context['success']:
        qw.save_quiz(name, description, questions, answers, image)
    return render(request, 'quiz_save_result.html', context=context)
