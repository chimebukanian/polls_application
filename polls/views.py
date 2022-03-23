from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import  generic
from django.utils import timezone


from .models import Question, Choice
# Create your views here.
class IndexView(generic.ListView):
    model=Question
    template_name='polls/index.html'
    context_object_name='latest_question_list'

    def get_queryset(self):
        """
        return the last 5 published questions(no future questions)
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model=Question
    template_name='polls/detail.html'
    def get_queryset(self):
        """
        excludes any questions that aren't published yet
        """ 
        return Question.objects.filter(pub_date__lte=timezone.now())
        
class ResultsView(generic.DetailView):
    model=Question
    template_name='polls/results.html'

def vote(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
        'question' : question,
        'error_message': "you didn't selet a choice!,"
            })
    else:
        selected_choice.votes+=1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

class CreateQuestion(CreateView):
    model=Question
    fields='__all__'
    success_url=reverse_lazy('polls:index')

class QuestionUpdate(UpdateView):
    model=Question
    fields='__all__'
    success_url=reverse_lazy('polls:index')
    
class QuestionDelete(DeleteView):
    model=Question
    success_url=reverse_lazy('polls:index')

class CreateChoice(CreateView):
    model=Choice
    fields='__all__'
    success_url=reverse_lazy('polls:index')

    def get_initial(self):
        initial=super().get_initial()
        initial['question']=self.request.GET.get('question_text')
        return initial

class ChoiceUpdate(UpdateView):
    model=Choice
    fields='__all__'
    success_url=reverse_lazy('polls:index')
    
class ChoiceDelete(DeleteView):
    model=Choice
    success_url=reverse_lazy('polls:index')