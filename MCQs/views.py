from django.shortcuts import render, redirect
from .models import Quiz
from lesson.models import Lesson
from lesson.urls import *
# Create your views here.

    

def addQuiz(request, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    if request.method == 'POST':
        question = request.POST.get('question')
        option_1 = request.POST.get('option_1')
        option_2 = request.POST.get('option_2')
        option_3 = request.POST.get('option_3')
        option_4 = request.POST.get('option_4')
        answer = request.POST.get('answer')

        quiz = Quiz.objects.create(question=question, option_1=option_1, option_2=option_2, option_3=option_3, option_4=option_4,
                                    answer=answer, in_lesson=lesson)
        quiz.save()
        return redirect('view_lesson', lesson_id)
    return render(request, 'MCQs/addQuiz.html')


    