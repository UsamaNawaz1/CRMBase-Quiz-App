from django.urls import path
from . import views


urlpatterns = [
    path('addQuiz/<str:lesson_id>/', views.addQuiz, name='addQuiz'),
]