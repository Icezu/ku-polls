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


class VotingTest(TestCase):
    """Test for voting."""

    def setUp(self):
        """Setup the test."""
        User.objects.create_user(username="User", password="Test@1234", email="User@hotmail.com")
        self.question = create_question(question_text="TestQuestion", start=-1, end=7)
        self.choice1 = self.question.choice_set.create(choice_text='Choice1')
        self.choice2 = self.question.choice_set.create(choice_text='Choice2')
        self.question_url = reverse('polls:vote', args=(self.question.id,))

    def test_response_code_unauthenticated_detail_page(self):
        """Unauthenticated user cannot access the detail page."""
        response = self.client.get(self.question_url)
        self.assertEqual(response.status_code, 302)

    def test_response_code_authenticated_detail_page(self):
        """Authenticated user can access detail page."""
        self.client.post(reverse('login'), {'username': 'User', 'password': 'Test@1234'}, follow=True)
        response = self.client.get(self.question_url)
        self.assertEqual(response.status_code, 200)
    