from random import shuffle

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from test_app.models import TestQuiz
from util.get_object_list_by_id import get_prepared_test
from .models import UserAnswers
from django.http import HttpResponse


@login_required
def pass_test(request, id_test):
    all_questions_and_answers = get_prepared_test(id_test)
    shuffle(all_questions_and_answers)
    displayed_questions_and_answers = all_questions_and_answers[:10]

    if request.method == "POST":
        for i in displayed_questions_and_answers:
            answer_id = request.POST.get(f"{i['question'].id}")
            UserAnswers.create_user_answer_by_user_and_ids(request.user, answer_id, id_test)
        return redirect('test_result', id_test=id_test)

    return render(request, 'test_passing.html', {
        'questions_and_answers': displayed_questions_and_answers,
        'current_test': TestQuiz.get_name_by_id(id_test)
    })


@login_required
def current_result(request, id_test):
    test = TestQuiz.get_test_by_id(id_test)
    result = UserAnswers.get_test_result(request.user, id_test)
    correct_answers = 0
    max_correct_answer = len(result)
    max_final_grade = 300.0
    for i in result:
        a = i.chosen_answer.is_correct
        if a:
            correct_answers += 1
    final_grade = (correct_answers / max_correct_answer) * max_final_grade
    if final_grade >= max_final_grade*0.6:
        response = 'Congratulations, you passed test'
    else:
        response = 'You failed, we hope you will pass next time'

    return render(request, 'passed_test_result.html', {'test': test,
                                                       'mark': correct_answers,
                                                       'max_mark': max_correct_answer,
                                                       'final_grade': final_grade,
                                                       'max_final_grade': max_final_grade,
                                                       'response': response
                                                       })


def available_test_list(request):
    users_tests = TestQuiz.objects.all()
    return render(request, 'available_tests.html', {'list': users_tests})
