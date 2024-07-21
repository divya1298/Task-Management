from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import Task
from .tasks import check_overdue_tasks
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


User = get_user_model()

class UserTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password')
        self.user.is_active = False
        self.user.save()

        # Generate activation link and token
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)
        self.activate_url = reverse('activate', args=[self.uidb64, self.token])

    def test_user_activation(self):
        response = self.client.get(self.activate_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

class TaskTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        self.client.force_authenticate(user=self.user)
        self.task_data = {
            'title': 'Test Task',
            'description': 'Task description',
            'due_date': timezone.now() + timedelta(days=1),
            'assigned_to': self.user.id,
        }

    def test_task_creation(self):
        response = self.client.post(reverse('task_list_create'), self.task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Task')

    def test_task_list(self):
        self.client.post(reverse('task_list_create'), self.task_data, format='json')
        response = self.client.get(reverse('task_list_create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_task_update(self):
        task = self.client.post(reverse('task_list_create'), self.task_data, format='json').data
        update_data = {'title': 'Updated Task'}
        response = self.client.patch(reverse('task_detail', args=[task['id']]), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Task')

    def test_task_deletion(self):
        task = self.client.post(reverse('task_list_create'), self.task_data, format='json').data
        response = self.client.delete(reverse('task_detail', args=[task['id']]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(reverse('task_list_create'))
        self.assertEqual(len(response.data), 0)

class CeleryTasksTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        self.task = Task.objects.create(
            title='Overdue Task',
            description='Task description',
            due_date=timezone.now() - timedelta(days=1),
            user=self.user,
            assigned_to=self.user
        )

    def test_check_overdue_tasks(self):
        from celery import current_app as celery
        celery.conf.update(task_always_eager=True)
        check_overdue_tasks()
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)
