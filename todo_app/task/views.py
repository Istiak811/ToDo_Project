from django.shortcuts import render, redirect
from . import models
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView,FormView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

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
    
class TaskCreate(LoginRequiredMixin, CreateView):
    model = models.Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    template_name = 'task/task_form.html'
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
class TaskDetail(LoginRequiredMixin, DetailView):
    model = models.Task
    context_object_name = 'task'
    template_name = 'task/task.html'

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = models.Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    template_name = 'task/task_form.html'


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = models.Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'task/task_delete.html'
    

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user = owner)
    

class CustomLoginView(LoginView):
    template_name = 'task/login.html'
    fields = '__all__'
    redirect_authenticated_user = True


    def get_success_url(self):
        return reverse_lazy('tasks')
    
class RegisterPage(FormView):
    template_name = 'task/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(request, *args, **kwargs)