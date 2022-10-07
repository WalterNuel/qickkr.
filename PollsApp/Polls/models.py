from calendar import week
import datetime
from email.mime import image

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Post(models.Model):
  post_text = models.TextField(max_length=250)
  pub_date = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, auto_created=True)
  upVotes = models.IntegerField(default=0)
  downVotes = models.IntegerField(default=0)

  def __str__(self):
    return self.post_text

  def time_posted(self):
        check = self.pub_date
        ago = timezone.now() - self.pub_date
        hours = f'{check.day}/{check.month}/{check.year}'

        if ago.days == 1:
          hours = 'Yesterday'

        elif ago.days < 1:
          if ago.seconds < 60:
            hours = 'Just Now'
          elif ago.seconds < (60 * 60):
            hours = 'Moments ago'
          else:
            hours = f'Today'

        return hours

# class Bio(models.model):
#   bio_text = models.TextField(max_length=150)
#   user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
#   likes = models.IntegerField(default=0)

class Comment(models.Model):
  comment_text = models.TextField(max_length=250)
  comment_date = models.DateField(auto_now_add=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  upVotes = models.IntegerField(default=0)
  downVotes = models.IntegerField(default=0)

  def __str__(self):
     return self.comment_text