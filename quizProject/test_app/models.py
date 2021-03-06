from django.db import models, IntegrityError
from account.models import CustomUser


# Create your models here.
class TestQuiz(models.Model):
    creator_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    test_name = models.CharField(max_length=30)

    def create_test_quiz(creator_id, test_name):
        test_quiz = TestQuiz(creator_id=creator_id, test_name=test_name)
        try:
            test_quiz.save()
            return test_quiz
        except (ValueError, IntegrityError):
            return None

    def __str__(self):
        return f'{self.test_name}'

    @staticmethod
    def get_name_by_id(id_test):
        current_test = TestQuiz.objects.get(id=id_test)
        return current_test.test_name

    @staticmethod
    def delete_quiz(id_test, user_id):
        try:
            TestQuiz.objects.filter(id=id_test, creator_id=user_id).delete()
        except (ValueError, IntegrityError):
            return None


class Questions(models.Model):
    question_text = models.CharField(max_length=100)
    answers_amount = models.IntegerField(default=4)
    one_correct_answer = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.question_text}'

    def create_question(question_text, answers_amount, one_correct_answer):
        question = Questions(question_text=question_text, answers_amount=answers_amount)
        try:
            question.save()
            return question
        except (ValueError, IntegrityError):
            return None


class AnswerOption(models.Model):
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=50)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.answer_text}'

    def create_answer(question, answer_text, is_correct):
        answer = AnswerOption(question_id=question, answer_text=answer_text, is_correct=is_correct)
        try:
            answer.save()
            return answer
        except (ValueError, IntegrityError):
            return None


class TestQuestionUnion(models.Model):
    test = models.ForeignKey(TestQuiz, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.test};{self.question}'

    @staticmethod
    def create_union(test, question):
        union = TestQuestionUnion(test=test, question=question)
        try:
            union.save()
            return union
        except (ValueError, IntegrityError):
            return None
