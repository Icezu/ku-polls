"""Django test for Django Model."""
from django.test import TestCase
# Create your tests here.
import datetime
from django.utils import timezone
from polls.models import Question


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


class QuestionModelTests(TestCase):
    """Tests for Django model."""

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently_() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True
        for questions whose pub_date is within
        the last day.
        """
        time = timezone.now() - datetime.timedelta(
                    hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_current_date(self):
        """
        is_published() return True if current date
        is on publication date.
        """
        time = timezone.now()
        current_question = Question(pub_date=time)
        self.assertIs(current_question.is_published(), True)

    def test_is_published_with_future_question(self):
        """
        is_published() return False if the polls
        publish date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=5)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_after_publication_date(self):
        """
        is_published() return True if the polls
        is published after published date.
        """
        time = timezone.now() - datetime.timedelta(days=3)
        past_question = Question(pub_date=time)
        self.assertIs(past_question.is_published(), True)

    def test_can_vote_before_published_date(self):
        """
        can_vote() return False if voting
        is allowed before the poll is published.
        """
        time = timezone.now() + datetime.timedelta(days=5)
        future_polls = Question(pub_date=time)
        self.assertIs(future_polls.can_vote(), False)

    def test_can_vote_during_published_date(self):
        """
        can_vote() return True if voting
        is allowed during the poll published and end date.
        """
        time = timezone.now() - datetime.timedelta(days=2)
        current_poll = Question(pub_date=time, end_date=timezone.now()
                                + datetime.timedelta(days=3))
        self.assertIs(current_poll.can_vote(), True)

    def test_can_vote_after_end_date(self):
        """
        can_vote() return False if voting
        is allowed after the poll has ended.
        """
        time = timezone.now() - datetime.timedelta(days=2)
        ended_poll = Question(pub_date=time, end_date=timezone.now()
                              - datetime.timedelta(days=1))
        self.assertIs(ended_poll.can_vote(), False)
