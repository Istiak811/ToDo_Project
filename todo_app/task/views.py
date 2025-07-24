from django.shortcuts import render
from . import models
from django.views.generic import ListView,CreateView,DetailView,UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def home(request):
    pass

class TaskList(LoginRequiredMixin, ListView):
    model = models.Task
    context_object_name = 'tasks'
    template_name = 'task/task_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Removed self parameter
        context['tasks'] = context['tasks'].filter(user=self.request.user)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)  # Fixed 'task' to 'tasks'
        context['search_input'] = search_input
        return context
    
class TaskCreate(CreateView):
    model = models.Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    template_name = 'task/task_form.html'
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
class TaskDetail(DetailView):
    model = models.Task
    context_object_name = 'task'
    template_name = 'task/task.html'

class TaskUpdate(UpdateView):
    model = models.Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    template_name = 'task/task_form.html'
