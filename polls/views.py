from django.shortcuts import get_object_or_404, render, redirect

# Create your views here.
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    """View index page."""
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including
        those set to be published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

@login_required
def vote_poll_error(request, pk):
    """
    Return a detail page if there're no errors or
    index page if there's error.
    """
    question = get_object_or_404(Question, pk=pk)
    user = request.user
    vote = get_vote_for_user(user, question)
    if not question.can_vote():
        messages.error(request, "Cannot vote this poll!")
        return redirect('polls:index')
    if vote is None:
        return render(request, 'polls/detail.html', {'question': question, 'current_choice': vote})
    else:
        return render(request, 'polls/detail.html', {'question': question, 'current_choice': vote.choice})

# class DetailView(generic.DetailView):
#     """View detail page."""
#     model = Question
#     template_name = 'polls/detail.html'

#     def get_queryset(self):
#         """Excludes any questions that aren't published yet."""
#         return Question.objects.filter(pub_date__lte=timezone.now())
    

class ResultsView(generic.DetailView):
    """View result page."""
    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """Update choice count when selecting."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # get previous vote from user
        user = request.user
        vote = get_vote_for_user(user, question)
        # case 1: user has not voted for this poll question yet
        # Create a new vote object
        if not vote:
            vote = Vote(user=user, choice=selected_choice)
        else:
            # case 2: user has already vote
            # Modify the existing vote and save it
            vote.choice = selected_choice
        vote.save()
        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question.id,)))


def get_vote_for_user(user, poll_question):
    """Find and return an existing vote for a user on a poll question.

    Returns:
        The user's Vote or None if no vote for this poll_question
    """
    votes = Vote.objects.filter(user=user).filter(choice__question=poll_question)
    # should be at most one Vote
    if votes.count() == 0:
        return None
    else:
        return votes[0]

