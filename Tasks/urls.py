from django.urls import path
from .views import CreateUserView, ActivateUserView, TaskListCreateView, TaskRetrieveUpdateDestroyView, MonitoringLogListView

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('activate/<uidb64>/<token>/', ActivateUserView.as_view(), name='activate'),
    path('tasks/', TaskListCreateView.as_view(), name='task_list_create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task_detail'),
   
]