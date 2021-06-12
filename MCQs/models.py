from django.db import models
from lesson.models import Lesson


class Quiz(models.Model):
    question = models.TextField(default='', null=False)
    option_1 = models.CharField(max_length=300, default='', null=False)
    option_2 = models.CharField(max_length=300, default='', null=False)
    option_3 = models.CharField(max_length=300, default='', null=False)
    option_4 = models.CharField(max_length=300, default='', null=False)
    answer = models.CharField(max_length=200, default='NA', null=False)
    in_lesson = models.ForeignKey(Lesson, related_name='questions', on_delete=models.CASCADE)


