from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import F
from django.utils import timezone

from .models import Question, Choice

# * old codes 3
# def index(request):
#     latest_quest = Question.objects.order_by('-pub_date')[:3]
#     ctx = {'latest_quest': latest_quest}

#     # * old codes 1
#     # template = loader.get_template('polls/index.html')
#     # return HttpResponse(template.render(ctx, request))
#     # * end of old codes 1
#     return render(request, 'polls/index.html', ctx)

# def detail(request, question_id):
#     # * old codes 2
#     # try:
#     #     q = Question.objects.get(id=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404('Question does not exist, dummy!')
#     # * end of old codes 2
#     q = get_object_or_404(Question, id=question_id)

#     ctx = {'quest': q}
#     return render(request, 'polls/detail.html', ctx)

# def results(request, question_id):
#     quest = get_object_or_404(Question, id=question_id)
#     return render(request, 'polls/results.html', {
#         'quest': quest
#     })
# * end of old codes 3


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_quest'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        now = timezone.now().astimezone(timezone.get_current_timezone())
        objs = Question.objects.filter(pub_date__lte=now)
        return objs.order_by('-pub_date')[:3]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_context_data(self, **kwargs):
        q = get_object_or_404(Question, id=kwargs.get('object').id)
        return {
            'quest': q,
            'choices': q.choices.all().order_by('pk')
        }

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        now = timezone.now().astimezone(timezone.get_current_timezone())
        return Question.objects.filter(pub_date__lte=now)


class ResultsView(generic.DetailView):
    model = Question
    context_object_name = 'quest'
    template_name = 'polls/results.html'


def vote(request, question_id):
    quest = get_object_or_404(Question, id=question_id)
    try:
        selected = quest.choices.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'quest': quest,
            'error_msg': 'You didnt select a choice.',
        })
    else:
        # * use F() to avoid race conditions
        selected.votes += 1
        selected.save()
        return HttpResponseRedirect(reverse(
            'polls:results', args=(quest.id,)))