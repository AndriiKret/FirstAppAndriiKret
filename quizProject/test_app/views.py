from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import TestQuiz, Questions, AnswerOption, TestQuestionUnion
from random import shuffle


@login_required
def tests_list(request):
    users_tests = TestQuiz.objects.filter(creator_id=request.user.id)
    return render(request, 'test_list.html', {'list': users_tests})


@login_required
def create_quiz(request):
    if request.method == 'POST':
        test_name = request.POST.get('test_name')
        test = TestQuiz.create_test_quiz(request.user, test_name=test_name)
        if test:
            return redirect('test_list')
    return render(request, 'quiz_creator.html')


@login_required
def delete_quiz(request, id_test):
    user_id = request.user.id
    TestQuiz.delete_quiz(id_test, user_id)
    return redirect('test_list')


def quiz_passing(request, id_test):
    questions_and_answers = _get_test(id_test)
    shuffle(questions_and_answers)
    return render(request, 'quiz_passing.html', {
        'questions_and_answers': questions_and_answers[:10],
        'current_test': TestQuiz.get_name_by_id(id_test)
    })


@login_required()
def view_test(request, id_test):
    questions_and_answers = _get_test(id_test)
    return render(request, 'view_text.html', {
        'questions_and_answers': questions_and_answers,
        'current_test': TestQuiz.get_name_by_id(id_test)
    })


@login_required
def add_question(request, id_test):
    current_test = TestQuiz.objects.get(pk=id_test)

    if request.method == "POST":
        question_text = request.POST.get('question_text')
        answers_amount = request.POST.get('answers_amount')
        one_correct_answer = request.POST.get('one_correct_answer')
        question = Questions.create_question(question_text, answers_amount, one_correct_answer)
        union = TestQuestionUnion.create_union(current_test, question)

        if union:
            return redirect('add_option_answers', id_question=question.id)

    return render(request, 'add_question.html')


@login_required
def add_options_to_question(request, id_question):
    current_question = Questions.objects.get(id=id_question)
    answer_amount = current_question.answers_amount

    if request.method == 'POST':
        for i in range(1, answer_amount + 1):
            answer_text = request.POST.get(f'answer_text_{i}')
            is_correct = request.POST.get(f'is_correct')
            print(is_correct)

            if is_correct == f'{i}':
                is_correct = True
            else:
                is_correct = False

            AnswerOption.create_answer(question=current_question, answer_text=answer_text,
                                       is_correct=is_correct)
            if i == answer_amount:
                return redirect('test_list')
    print(answer_amount)

    return render(request, 'add_answers.html', {
        'id_question': id_question,
        'answer_amount': list(range(1, answer_amount + 1)),
    })


def _get_test(id_test):
    # current_test = TestQuiz.objects.get(id=id_test)
    union = TestQuestionUnion.objects.filter(test_id=id_test)
    questions_and_answers = []
    for i in union:
        q = Questions.objects.get(id=i.question_id)
        questions_and_answers.append({
            'question': q,
            'answer_option': q.answeroption_set.all()
        })
    return questions_and_answers
