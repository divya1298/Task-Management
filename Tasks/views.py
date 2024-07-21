from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Task, MonitoringLog
from .serializers import UserSerializer, TaskSerializer, MonitoringLogSerializer
from .tasks import check_overdue_tasks

User = get_user_model()

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(username=request.data['username'])
        if not user.is_active:
            self.send_activation_email(user)
        return response

    def send_activation_email(self, user):
        subject = 'Activate Your Account'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = self.request.build_absolute_uri(reverse('activate', args=[uid, token]))

        html_message = render_to_string('email/activation_email.html', {
            'user': user,
            'activation_link': activation_link
        })
        plain_message = strip_tags(html_message)
        from_email = 'no-reply@yourdomain.com'
        to_email = user.email

        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

class ActivateUserView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Account activated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Activation link is invalid.'}, status=status.HTTP_400_BAD_REQUEST)

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class MonitoringLogListView(generics.ListAPIView):
    queryset = MonitoringLog.objects.all()
    serializer_class = MonitoringLogSerializer
