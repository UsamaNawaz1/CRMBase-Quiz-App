from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import Attempts, Lesson, Intro, Blocks, UserProfile
from MCQs.models import Quiz
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    lessons = Lesson.objects.all()
    context = {
        'lessons':lessons,
    }
    return render(request, 'lesson/home.html', context)

@login_required(login_url='login')
def addLesson(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        estimated_time = request.POST.get('estimated_time')
        video_url = request.POST.get('video_url')
        lesson_content = request.POST.get('lesson_content')
        intro_title = request.POST.get('intro_title')
        description = request.POST.get('description')
        objectives = request.POST.get('objectives')
        intro = Intro.objects.create(intro_title=intro_title,description=description, objectives=objectives)
        intro.save()
        lesson = Lesson.objects.create(title=title, intro=intro,lesson_content=lesson_content, video_url=video_url, estimated_time=estimated_time)
        lesson.save()
        users =User.objects.all()
        for user in users:
            attempt = Attempts.objects.create(made_by=user, on_lesson=lesson)
            attempt.save()
        block = Blocks.objects.create(block_title='Lesson Introduction', block_content=description, lesson=lesson)
        block.save()
        return redirect('home')
    

    return render(request, 'lesson/addLesson.html')

@login_required(login_url='login')
def view_lesson(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    questions = Quiz.objects.filter(in_lesson=lesson)
    blocks = Blocks.objects.filter(lesson=lesson)[1:]
    data = dict()
    try:
        attempt = Attempts.objects.get(made_by=request.user, on_lesson=lesson)
    except:
        attempt = Attempts.objects.create(made_by=request.user, on_lesson=lesson)
    correct_answers = 0
    points = 0
    if request.method == 'POST':
        for question in questions:
            selected_option = request.POST.get(f'option{question.id}')
            if selected_option == question.answer:
                correct_answers += 1
        
        if correct_answers == len(questions):
            if attempt.attempts == 0:
                request.user.userprofile.points += 100
                points = 100
            elif attempt.attempts == 1:
                request.user.userprofile.points += 50
                points = 50
            else:
                request.user.userprofile.points += 25
                points = 25
            request.user.userprofile.save()
            messages.success(request, f"You have successfully passed the quiz. We have awarded you {points} points")
            
        else:
            attempt.attempts += 1
            attempt.save()
            messages.error(request, "Unfortunately, there are one or more mistakes. Please review the lesson and try again.")


    context ={
        'lesson':lesson,
        'blocks':blocks,
        'questions':questions,
        'data':data,
    }
    return render(request, 'lesson/view_lesson.html', context)

@login_required(login_url='login')
def addBlock(request, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    if request.method == 'POST':
        block_title = request.POST.get('block_title')
        block_content = request.POST.get('block_content')

        block = Blocks.objects.create(block_title=block_title, block_content=block_content, lesson=lesson)
        block.save()
        return redirect('view_lesson', lesson_id)
    
    return render(request, 'lesson/addBlock.html')


def registerPage(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.email = request.POST.get('email')
            user.save()
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            userprofile = UserProfile.objects.create(user = user, first_name=first_name, last_name=last_name)
            userprofile.save()
        
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'lesson/register.html', {'form':form})


def loginPage(request):
    data = dict()
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            
            messages.error(request, "username or password is incorrect")
 
    return render(request, 'lesson/login1.html', data)

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('login')