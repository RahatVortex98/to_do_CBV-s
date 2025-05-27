from django.shortcuts import redirect, render

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView

from django.contrib.auth.views import LoginView

from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login

from django.urls import reverse_lazy
from .models import Task


class TaskLogin(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')
    
class Registration(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True

    success_url = reverse_lazy('tasks')
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super().form_valid(form)
    

class GetLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)



    
    
    

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        search_input = self.request.GET.get('search-area') or ''
        queryset = Task.objects.filter(user=self.request.user)

        if search_input:
            queryset = queryset.filter(title__icontains=search_input)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = self.get_queryset().filter(complete=False).count()
        context['search_input'] = self.request.GET.get('search-area') or ''
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task 
    template_name = 'task_detail.html'
    context_object_name = 'task'



class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    template_name = 'task_create.html'
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user  # 🔐 Force secure ownership
        return super(TaskCreate,self).form_valid(form)

    
    
    
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    template_name = 'task_create.html'
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')
    
class Taskdelete(LoginRequiredMixin,DeleteView):
    model = Task
    template_name = 'task_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    
    

