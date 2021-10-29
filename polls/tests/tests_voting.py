"""Django test for voting."""
import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from polls.models import Question, Vote
from django.contrib.auth.models import User


def create_question(question_text, start, end):
    """
    Create a question with the given 'question_text' and published the
    given number of 'days' offset to now (negative for questions published
    in the past, positive for questions that have yet to be published.)
    """
    time = timezone.now() + datetime.timedelta(days=start)
    end_time = timezone.now() \
        + datetime.timedelta(days=end)
    return Question.objects.create(question_text=question_text,
                                   pub_date=time, end_date=end_time)


# class VotingTest(TestCase):
#     """Test for voting."""

    