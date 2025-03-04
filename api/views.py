from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from main.models import (
    UserSay,
    Course, CustomUser, Teacher, CourseStudent
)

from rest_framework import generics
from .serializers import UserSaySerializer, CourseSerializer, TeacherSerializer

# Create your views here.

# class UserSayListAPI(generics.ListCreateAPIView):
#     queryset = UserSay.objects.all()
#     serializer_class = UserSaySerializer

class UserSayListAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_says = UserSay.objects.all()
        serializer = UserSaySerializer(user_says, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSayDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request, pk):
        user_say = get_object_or_404(UserSay, pk=pk)
        serializer = UserSaySerializer(user_say)
        return Response(serializer.data)

    def put(self, request, pk):
        user_say = get_object_or_404(UserSay, pk=pk)
        if request.user != user_say.user:
            return Response({"detail": "Siz ushbu Commentni tahrirlay olmaysiz!"},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = UserSaySerializer(user_say, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user_say = get_object_or_404(UserSay, pk=pk)
        if request.user != user_say.user:
            return Response({"detail": "Siz ushbu Commentni O'chira  olmaysiz!"},
                            status=status.HTTP_403_FORBIDDEN)

        user_say.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CourseListAPI(APIView):

    def get(self, request):
        if not request.user.is_authenticated:
            courses = Course.objects.all()
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data)
        else:
            if request.user.role == "STUDENT":
                courses = Course.objects.all()
                serializer = CourseSerializer(courses, many=True)
                return Response(serializer.data)
            elif request.user.role == "TEACHER":
                courses = Course.objects.filter(teacher__user=request.user)
                serializer = CourseSerializer(courses, many=True)
                return Response(serializer.data)

            elif request.user.role == "ADMIN":
                courses = Course.objects.all()
                serializer = CourseSerializer(courses, many=True)
                return Response(serializer.data)
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Siz ro‘yxatdan o‘tmagansiz!"},
                                status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.is_authenticated and request.user.role == "TEACHER":
            serializer = CourseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDetailAPI(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        course = get_object_or_404(Course,pk=pk)
        if not request.user.role == "TEACHER":
            return Response(
                {"detail": "Siz Kursni tahrir qila olmaysiz!"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        elif request.user.role == "TEACHER":
            if request.user == course.teacher.user:
                serializer = CourseSerializer(course, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = get_object_or_404(Course,pk=pk)

        if not request.user.role == "TEACHER":
            return Response(
                {"detail": "Siz Kursni tahrir qila olmaysiz!"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        elif request.user.role == "TEACHER":
            if request.user == course.teacher.user:
                course.delete()
                return Response({
                    "detail": "Kurs o'chirildi!"
                },
                    status=status.HTTP_204_NO_CONTENT
                )





class TeacherListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == "STUDENT":
            teacher = CourseStudent.objects.filter(student=request.user).first()
            serializer = TeacherSerializer(teacher,many=True)
            return Response(serializer.data)
        elif request.user.role == "TEACHER":
            teacher = Teacher.objects.get(user=request.user)
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data)
        elif request.user.role == "ADMIN":
            teachers = Teacher.objects.all()
            serializer = TeacherSerializer(teachers, many=True)
            return Response(serializer.data)


class TeacherDetailAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request, pk):
        teacher = Teacher.objects.get(user=pk)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)


