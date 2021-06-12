from django.db import models
from django.contrib.auth.models import User



class Intro(models.Model):
    intro_title = models.CharField(max_length=300, null=False, default='')
    description = models.TextField(null=False, default='')
    objectives = models.TextField(null=False, default='')


class Lesson(models.Model):
    title = models.CharField(max_length=300, null=False, default='')
    intro = models.ForeignKey(Intro, related_name='blocks', on_delete=models.CASCADE)
    video_url = models.CharField(max_length=200, null=True)
    lesson_content = models.TextField(null=False, default='')
    estimated_time = models.CharField(max_length=100, null=False, default='')

class Blocks(models.Model):
    block_title = models.CharField(max_length=300, null=False, default='')
    block_content = models.TextField(null=False, default='')
    lesson = models.ForeignKey(Lesson, related_name='blocks', on_delete=models.CASCADE)
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="userprofile", on_delete=models.CASCADE)
    
    first_name = models.CharField(max_length=100, blank=False, null=False, default='')
    last_name = models.CharField(max_length=100, blank=False, null=False, default='')
    points = models.IntegerField(default=0)
    
class Attempts(models.Model):
    attempts = models.IntegerField(default=0)
    made_by = models.ForeignKey(User, related_name='attempts', on_delete=models.CASCADE)
    on_lesson = models.ForeignKey(Lesson, related_name='quizattempts', on_delete=models.CASCADE)
    