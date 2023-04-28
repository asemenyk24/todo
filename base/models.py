from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
	"""Модель задачи, которую необходимо выполнить пользователю."""
	user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)
	title = models.CharField(max_length = 80)
	description = models.TextField(max_length = 400, null = True, blank = True)
	completion = models.BooleanField(default = False)
	date_added = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		# Текстовое представление задачи.
		return self.title

	class Meta:
		# Сортировка по выполнению.
		ordering = ['completion']