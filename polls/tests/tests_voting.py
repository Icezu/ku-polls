# """Django test for voting."""
# import datetime
# from django.test import TestCase
# from django.utils import timezone
# from django.urls import reverse
# from polls.models import Question, Vote
# from django.contrib.auth.models import User


# def create_question(question_text, start, end):
#     """
#     Create a question with the given 'question_text' and published the
#     given number of 'days' offset to now (negative for questions published
#     in the past, positive for questions that have yet to be published.)
#     """
#     time = timezone.now() + datetime.timedelta(days=start)
#     end_time = timezone.now() \
#         + datetime.timedelta(days=end)
#     return Question.objects.create(question_text=question_text,
#                                    pub_date=time, end_date=end_time)

# # TODO fix test
# # class VotingTest(TestCase):
# #     """Test for voting."""

# #     def test_can_vote_when_authorize(self):
# #         """Only authorized user can vote on a question."""
# #         question = create_question(question_text="test question", start=-1, end=5)
# #         choice = question.choice_set.create(choice_text="test choice 1")
# #         user = User.objects.create_user(
# #             username='test',
# #             password='Test@1234',
# #             email='test@gmail.com')
# #         question.vote_set.create(user=user, question=question, choice=choice)
# #         response = self.client.post(reverse('login'),
# #                                     {'username': 'test',
# #                                      'password': 'Test@1234'},
# #                                     follow=True)
# #         url = reverse("polls:detail", args=(question.id,))
# #         response = self.client.get(url)
# #         self.assertEqual(response.status_code, 200)
# #         self.client.post(reverse('polls:vote', args=(question.id,)), {'choice': 1})
# #         self.assertEqual(Vote.objects.filter(question=question, choice=choice).count(), 1)
