from django.db import models

# Create your models here.
import datetime

from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Django model Object for questions."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end_date')

    def was_published_recently(self):
        """Check if question was published recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def is_published(self):
        """Check if question is published."""
        now = timezone.now()
        return self.pub_date <= now

    def can_vote(self):
        """Check if you can vote."""
        now = timezone.now()
        return self.pub_date <= now <= self.end_date and self.is_published()

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    """Django model Object for choices."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    # we want to be able to  write 'choice.votes' in our views
    # and templates to get the number of votes for a Choice.
    # We want the existing code to still work.
    @property
    def votes(self):
        count = Vote.objects.filter(choice=self).count()
        return count


class Vote(models.Model):
    # specify id
    # id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"Vote by {self.user} for {self.choice.choice_text} on question {self.choice.question} "
