from django.contrib.auth.models import Group
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     RetrieveAPIView, get_object_or_404, CreateAPIView,
                                     UpdateAPIView, )
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task, User, ROLES
from .permissions import IsUserCustomer, IsUserAdmin, IsOwner, IsNoEmployer, IsUserEmployer, UpdateDoneTask
from .serializers import TaskSerializer, UserSerializer


class TaskCloseView(APIView):
    model = Task
    serializer_class = TaskSerializer
    permission_classes = (IsUserAdmin | IsOwner,)

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        if task.report is not None and not task.is_done():
            task.date_closed = timezone.now()
            task.status = Task.STATUS_DONE
            task.save()
            return Response({"msg": "Success"}, status.HTTP_204_NO_CONTENT)
        return Response({"msg": "Cannot end task"})


class TaskDetailView(UpdateAPIView, RetrieveAPIView):
    model = Task
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, IsUserAdmin | IsOwner | IsNoEmployer, UpdateDoneTask)

    def get_object(self):
        task = get_object_or_404(self.model, pk=self.kwargs.get("pk"))
        self.check_object_permissions(self.request, task)
        return task

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        if task.employer is None and task.is_active():
            task.employer = request.user
            task.status = task.STATUS_ACTIVE
            task.save()
            return Response({"msg": "Success"}, status.HTTP_204_NO_CONTENT)
        return Response({"error": "Task already have a employer"}, status.HTTP_409_CONFLICT)


class TaskListView(ListAPIView, CreateAPIView):
    model = Task
    queryset = Task.objects.filter(status=Task.STATUS_WAITING)
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer
    pagination_class = PageNumberPagination
    page_size = 20

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name=ROLES.EMPLOYER).exists():
            return Task.objects.filter(status=Task.STATUS_WAITING)
        return Task.objects.filter(customer=user)

    def post(self, request, *args, **kwargs):
        task = self.serializer_class(data=request.data)
        if task.is_valid(raise_exception=True):
            if request.user.groups.filter(name=ROLES.EMPLOYER) and task.customer is None:
                return Response({"msg": "You must point employer"}, status.HTTP_400_BAD_REQUEST)
            task.save(customer=request.data.pop('customer', None),
                      employer=request.data.pop('employer', None))
        return Response({"msg": "Success"}, status.HTTP_201_CREATED)


class EmployersList(ListAPIView):
    queryset = User.objects.filter(groups__name=ROLES.EMPLOYER)
    serializer_class = UserSerializer
    permission_classes = (IsUserCustomer,)
    pagination_class = PageNumberPagination
    page_size = 20


class UserListCreateView(ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsUserAdmin | IsUserEmployer,)

    def get(self, request, *args, **kwargs):
        return Response(UserSerializer(User.objects.all(), many=True).data, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        group = request.data.pop('group', None)
        if group in ROLES.roles:
            user = self.serializer_class(data=request.data)
            if user.is_valid(raise_exception=True):
                user.save()
                user = user.get_user()
                user.groups.add(Group.objects.filter(name=group).first())
                user.save()
        else:
            raise ValidationError([{"error": "field 'group' must be 'employer' or 'customer'"}])
        return Response({"msg": "Success"}, status.HTTP_201_CREATED)


class UserView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get('pk'))
        return Response(UserSerializer(user).data, status.HTTP_200_OK)


class MeView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response(UserSerializer(request.user).data, status.HTTP_200_OK)


class MyTasksView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer
    model = Task

    def get(self, request, *args, **kwargs):
        user = request.user
        tasks = user.employer_tasks if user.groups.filter(name=ROLES.EMPLOYER) else user.customer_tasks
        return Response(self.serializer_class(tasks, many=True).data, status.HTTP_200_OK)
