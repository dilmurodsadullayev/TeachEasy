from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from main.models import (
    UserSay,
    Course, CustomUser,Teacher
)

from rest_framework import generics
from .serializers import UserSaySerializer, CourseSerializer, TeacherSerializer

# Create your views here.

class UserSayListAPI(generics.ListAPIView):
    queryset = UserSay.objects.all()
    serializer_class = UserSaySerializer


class CourseListAPI(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class TeacherListAPI(generics.ListAPIView):
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        role = user.role

        if role == "ADMIN":
            return CustomUser.objects.filter(role='TEACHER')
        elif role == "TEACHER":
            return CustomUser.objects.filter(id=user.id)
        elif role == "STUDENT":
            pass

