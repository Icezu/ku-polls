"""Django test for detail view."""
import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from polls.models import Question
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


class QuestionDetailViewTests(TestCase):
    """Tests for detail page"""

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.',
                                          start=5, end=10)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the quesion's text.
        """
        past_question = create_question(question_text='Past Question.',
                                        start=-5, end=-2)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
