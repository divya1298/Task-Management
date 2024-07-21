from celery import shared_task
from .models import Task
from django.utils import timezone
from django.core.mail import send_mail

@shared_task
def check_overdue_tasks():
    now = timezone.now()
    overdue_tasks = Task.objects.filter(due_date__lt=now, completed=False)
    for task in overdue_tasks:
        send_mail(
            'Task Overdue',
            f'The task "{task.title}" is overdue. Please complete it as soon as possible.',
            'your-email@example.com',
            [task.user.email],
            fail_silently=False,
        )
        task.completed = True  
        task.save()
