from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import User, Task


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserSerializer(serializers.ModelSerializer):
    user = None
    password = serializers.CharField(write_only=True)
    group = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "surname",
                  "email", "last_login", "is_superuser",
                  "is_staff", "is_active", "date_joined",
                  "phone_number", "group", "password")

    def create(self, validated_data, *args, **kwargs):
        self.user = self.Meta.model.objects.create_user(email=validated_data.get("email"),
                                                        password=validated_data.get("password"))
        return self.user

    def get_user(self):
        return self.user


class TaskSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    employer = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'task_goal', 'status', 'report',
                  'date_created', 'date_updated', 'date_closed',
                  'employer', 'customer')

    def create(self, validated_data):
        employer = validated_data.pop("employer", None)
        customer = validated_data.pop("customer", None)
        if employer:
            employer = User.objects.get(employer)
        if customer:
            customer = User.objects.get(pk=customer)
        task = Task.objects.create(task_goal=validated_data.get("task_goal"), customer=customer, employer=employer)

        return task

    def update(self, instance, validated_data):
        instance.employer = validated_data.pop("employer", instance.employer)
        instance.customer = validated_data.pop("customer", instance.customer)
        instance.task_goal = validated_data.pop("task_goal", instance.task_goal)
        instance.status = validated_data.pop("status", instance.status)
        instance.report = validated_data.pop("report", instance.report)
        instance.save()
        return instance
