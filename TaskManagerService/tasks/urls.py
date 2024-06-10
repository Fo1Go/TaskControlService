from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from django.urls import path

from .views import (TaskListView, UserListCreateView, EmployersList,
                    UserView, TaskDetailView, MeView, MyTasksView, TaskCloseView)


urlpatterns = [
    path('tasks', TaskListView.as_view(), name='task_list'),
    path('tasks/<int:pk>', TaskDetailView.as_view(), name='get_task'),
    path('tasks/<int:pk>/close', TaskCloseView.as_view(), name='close_task'),
    path('employers', EmployersList.as_view(), name='employers_list'),
    path('users', UserListCreateView.as_view(), name='users'),
    path('me', MeView.as_view(), name='me'),
    path('me/tasks', MyTasksView.as_view(), name='me'),
    path('users/<int:pk>', UserView.as_view(), name='user_by_id'),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_obtain_pair'),
]
