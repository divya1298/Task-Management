from django.conf import settings
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks', default=1)  # Provide a default user ID
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assigned_tasks', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class MonitoringLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    checked_at = models.DateTimeField(auto_now_add=True)
    action_taken = models.BooleanField(default=False)

    def __str__(self):
        return f"Log for task {self.task.title} at {self.checked_at}"        