from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils.representation import serializer_repr
from rest_framework.views import APIView
from rest_framework import status
from datetime import date

from main.models import (
    UserSay,
    Course, CustomUser, Teacher, CourseStudent, JoinRequest, Student, CourseTask, Attendance
)

from rest_framework import generics
from .serializers import UserSaySerializer, CourseSerializer, TeacherSerializer, JoinRequestSerializer, \
    CourseTaskSerializer, CourseAttendanceSerializer, ProfileSerializer


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
        user = request.user
        user_data = CustomUser.objects.get(id=user.id)
        if serializer.is_valid():
            # serializer_data = serializer.data["user_data"]
            serializer.save(user=user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSayDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request, pk):
        user_say = get_object_or_404(UserSay, pk=pk)
        serializer = UserSaySerializer(user_say)
        return Response(serializer.data)

    # def put(self, request, pk):
    #     user_say = get_object_or_404(UserSay, pk=pk)
    #     if request.user != user_say.user:
    #         return Response({"detail": "Siz ushbu Commentni tahrirlay olmaysiz!"},
    #                         status=status.HTTP_403_FORBIDDEN)
    #
    #     serializer = UserSaySerializer(user_say, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


class JoinRequestListAPI(APIView):
    permission_classes = [IsAuthenticated]
    # def get(self, request, teacher_id):
    #     for i in range(3):
    #         course_teache = Course.objects.get(teacher=teacher_id)
    #         print(course_teache)
    #
    #     # print(course_teache)
    #     course_teacher = Course.objects.get(teacher=teacher_id)
    #     if request.user.role == "TEACHER":
    #         join_request_data = []
    #         # for
    #         join_requests = JoinRequest.objects.filter(course=course_teacher)
    #         if join_requests:
    #             serializer = JoinRequestSerializer(join_requests, many=True)
    #             return Response(serializer.data)
    #         return Response({"message": "So'rov yuborgan student lar yo'q"}, status=status.HTTP_404_NOT_FOUND)
    #
    #
    #     else:
    #         return Response({"message": "Siz ushbu amalni qila olmaysiz!"},status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request,course_id , student_id): # bu yerda student shu kursga so'rov yuborgami shuni tekshiramiz
        course = Course.objects.get(id=course_id)
        student = Student.objects.get(user=student_id)
        student_join_request = JoinRequest.objects.filter(course=course, student=student).first()
        if student_join_request:
            serializer = JoinRequestSerializer(student_join_request)
            return Response(serializer.data)
        else:
            return Response({"message": "Siz bu kursga qo'shilish so'robvini yubormadingiz!"},
                            status=status.HTTP_404_NOT_FOUND)


    def post(self, request, course_id, student_id):
        if request.user.role == "STUDENT":
            student = Student.objects.get(user=student_id)
            course = Course.objects.get(id=course_id)
            serializer = JoinRequestSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(course=course, student=student)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Sizni ro'lingiz Student emas!"},
                            status=status.HTTP_404_NOT_FOUND)



class JoinRequestListsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(user=teacher_id)
        course_teacher = Course.objects.filter(teacher=teacher).first()
        # print(course_teacher)
        if request.user.role == "TEACHER":
            join_request_data = []
            # for
            join_requests = JoinRequest.objects.filter(course=course_teacher)
            if join_requests:
                serializer = JoinRequestSerializer(join_requests, many=True)
                return Response(serializer.data)
            return Response({"message": "So'rov yuborgan student lar yo'q"}, status=status.HTTP_404_NOT_FOUND)


        else:
            return Response({"message": "Siz ushbu amalni qila olmaysiz!"},status=status.HTTP_401_UNAUTHORIZED)





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

    def get(self, request, pk):
        teacher = get_object_or_404(Teacher, pk=pk)

        if teacher:
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data)
        else:
            Response({"message": "Bu id dagi Teacher topilmadi"},status=status.HTTP_404_NOT_FOUND)


class CourseTasksAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        if request.user.id == course.teacher.user.id:
            tasks = CourseTask.objects.filter(course=course).all()
            if tasks:
                serializer = CourseTaskSerializer(tasks, many=True)
                return Response(serializer.data)
            else:
                return Response({"message": "Tasklar yo'q!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Siz ushbu kursni ko'raolmaysiz!"},
                            status=status.HTTP_403_FORBIDDEN)

    def post(self, request, course_id):
        today = date.today()
        format_date = today.strftime("%Y-%m-%d")
        course = get_object_or_404(Course, pk=course_id)

        if not request.user.role == "TEACHER":
            return Response({"detail": "Siz Teacher emassiz!"},
                            status=status.HTTP_403_FORBIDDEN)

        elif request.user.role == "TEACHER":
            if request.user.id == course.teacher.user.id:
                serializer = CourseTaskSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(course=course, given_date=format_date)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                Response({"message": "Siz bu kursni tasklarini tahrir qilaolmaysiz"}, status=status.HTTP_403_FORBIDDEN)


class CourseTaskEditAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, course_id, task_id):
        if not request.user.role == "TEACHER":
            return Response(
                {"detail": "Siz taskni tahrirlay olmaysiz!"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        elif request.user.role == "TEACHER":
            course = get_object_or_404(Course, pk=course_id)
            if request.user.id == course.teacher.user.id:
                task = CourseTask.objects.get(id=task_id, course=course)
                serializer = CourseTaskSerializer(task, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Siz ushbu kursni tasklarini tahrirlayolmaysiz!"}, status=status.HTTP_403_FORBIDDEN)


    def delete(self,request, course_id, task_id):
        course = get_object_or_404(Course, pk=course_id)
        task = CourseTask.objects.get(id=task_id, course=course)

        if not request.user.role == "TEACHER":
            return Response(
                {"detail": "Siz taskni o'chira olmaysiz!"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        elif request.user.role == "TEACHER":
            if request.user.id != course.teacher.user.id:
                return Response({"detail": "Siz ushbu taskni O'chira  olmaysiz!"},
                                status=status.HTTP_403_FORBIDDEN)

            else:
                task.delete()
                return Response({"message": "Task o'chirilid"}, status=status.HTTP_204_NO_CONTENT)


class CourseAttendancesAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        if request.user.id == course.teacher.user.id:
            attendance = Attendance.objects.filter(course=course)
            # print(attendance)
            serializer = CourseAttendanceSerializer(attendance,many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "Siz bu kursni davomatini ko'ra olmaysiz"}, status=status.HTTP_403_FORBIDDEN)

# Profile API

class ProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == "TEACHER":
            user = get_object_or_404(CustomUser,pk=request.user.id)
            # courses = Course.objects.filter(teacher__user=user).all()
            serializer = ProfileSerializer(user)
            return Response(serializer.data)

        elif request.user == "STUDENT":
            pass