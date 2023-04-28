from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Task


class CustomLoginView(LoginView):
	"""Страница авторизации пользователья."""
	template_name = 'base/login.html'
	fields = '__all__'
	# Перенаправление пользователя, если он уже авторизован.
	redirect_authenticated_user = True

	def get_success_url(self):
		"""Функция перенаправления."""
		return reverse_lazy('tasks')


class RegisterPage(FormView):
	"""Страница регистрации пользователя."""
	template_name = 'base/register.html'
	form_class = UserCreationForm
	redirect_authenticated_user = True
	success_url = reverse_lazy('tasks')

	def form_valid(self, form):
		user = form.save()
		if user is not None:
			login(self.request, user)
		return super(RegisterPage, self).form_valid(form)

	def get(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('tasks')
		return super(RegisterPage, self). get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
	"""Представляет список задач."""
	model = Task
	context_object_name = 'tasks'

	def get_context_data(self, **kwargs):
		"""Ограничение, позволяет пользователю получать только свои задачи."""
		context = super().get_context_data(**kwargs)
		context['tasks'] = context['tasks'].filter(user = self.request.user)
		context['count'] = context['tasks'].filter(completion = False).count()

		search_input = self.request.GET.get('search-area') or ''
		if search_input:
			context['tasks'] = context['tasks'].filter(title__startswith = search_input)
		return context


class TaskCreate(LoginRequiredMixin, CreateView):
	"""Создать новую задачу."""
	model = Task
	fields = ['title', 'description', 'completion']
	success_url = reverse_lazy('tasks')

	def form_valid(self, form):
		# Не позволяет пользователю создавать задачи для других пользователей.
		form.instance.user = self.request.user
		return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
	"""Редактирование задачи."""
	model = Task
	fields = ['title', 'description', 'completion']
	success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
	"""Удаление задачи."""
	model = Task
	context_object_name = 'task'
	success_url = reverse_lazy('tasks')
	template_name = 'base/task_delete.html'
