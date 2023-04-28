from django.urls import path
from .views import TaskList, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView


urlpatterns = [
	# Страница авторизации пользователя.
	path('login/', CustomLoginView.as_view(), name = 'login'),
	# Выход пользователя из приложения.
	path('logout/', LogoutView.as_view(next_page = 'login'), name = 'logout'),
	# Страница регистрации пользователя.
	path('register/', RegisterPage.as_view(), name = 'register'),
	# Страница со всеми задачами.
	path('', TaskList.as_view(), name = 'tasks'),
	# Страница создания новой задачи.
	path('task-create/', TaskCreate.as_view(), name = 'task-create'),
	# Страница для редактирования задачи.
	path('task-update/<int:pk>/', TaskUpdate.as_view(), name = 'task-update'),
	# Страница удаления задачи.
	path('task-delete/<int:pk>/', TaskDelete.as_view(), name = 'task-delete'),
]
