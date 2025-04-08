from django.shortcuts import get_object_or_404

from main.models import UserSay, Course, Teacher, CustomUser, UserRoleEnum, JoinRequest, CourseTask,Attendance,Mark
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass


class UserSaySerializer(serializers.ModelSerializer):
    user_data = serializers.SerializerMethodField(method_name='users_data')

    class Meta:
        model = UserSay
        fields = ['id', 'user', 'message', 'created_time', 'user_data']
        extra_kwargs = {'user': {'read_only': True}}

    def users_data(self, obj):
        try:
            user = obj.user
            return {
                "id": user.id,
                "username": user.username,
                "image": user.image.url if user.image else None,
            }
        except CustomUser.DoesNotExist:
            return None


class CourseSerializer(serializers.ModelSerializer):
    teacher_data = serializers.SerializerMethodField(method_name="teachers_data")
    # join_request = serializers.SerializerMethodField(method_name="join_requests")
    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'description',
            'image',
            'price',
            'start_time',
            'end_time',
            'schedule_days',
            'teacher_data',

        ]

    def teachers_data(self, obj):
        try:
            teacher = obj.teacher
            return {
                "user": teacher.user.id,
                "username": teacher.user.username,
                "first_name": teacher.user.first_name,
                "last_name": teacher.user.last_name,
                "image": teacher.user.image.url if teacher.user.image else None,
                "phone_number": teacher.phone_number if hasattr(teacher, "phone_number") else None,
                "address": teacher.user.address,

            }
        except CustomUser.DoesNotExist:
            None

    # def join_requests(self,obj):
    #     course = obj.course
    #     user = self.request.user
    #     join_request = JoinRequest()
    #
    #     return {
    #
    #     }


class JoinRequestSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField(method_name="student_data")
    course = serializers.SerializerMethodField(method_name="course_data")

    class Meta:
        model = JoinRequest
        fields = ["id", "student", "course", "is_sent", "joinded"]

    def student_data(self, obj):
        student = obj.student
        # print(student)
        return {
            "id": student.user.id,
            "username": student.user.username
        }

    def course_data(self, obj):
        course = obj.course

        return {
            "id": course.id,
            "name": course.name,
            "image": course.image.url if course.image else None,
            "teacher": course.teacher.user.username,
            "email": course.teacher.user.email if course.teacher.user.email else None
        }


class TeacherCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "name"]


class TeacherSerializer(serializers.ModelSerializer):
    teacher_data = serializers.SerializerMethodField(method_name="get_teacher_data")
    courses = serializers.SerializerMethodField(method_name="get_courses")

    class Meta:
        model = Teacher
        fields = ['teacher_data', 'courses']

    def get_teacher_data(self, obj):
        teacher = obj

        return {
            "id": teacher.id,
            "username": teacher.user.username,
            "first_name": teacher.user.first_name,
            "last_name": teacher.user.last_name,
            "address": teacher.user.address,
            "birth_date": teacher.user.birth_date,
            "image": teacher.user.image.url if teacher.user.image else None
        }

    def get_courses(self, obj):
        return TeacherCourseSerializer(obj.courses.all(), many=True).data



class CourseTaskSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField(method_name="course_data")
    given_date = serializers.DateField(required=False)
    class Meta:
        model = CourseTask
        fields = ["id","course", "task_name", "definition", "given_date", "until_date", "is_done"]

    def course_data(self, obj):
        course = obj.course

        return {
            "id": course.id,
            "name": course.name,
            # "image": course.image.url if course.image else None,
            # "teacher": course.teacher.user.username,
            # "email": course.teacher.user.email if course.teacher.user.email else None
        }


class CourseAttendanceSerializer(serializers.ModelSerializer):
    marks = serializers.SerializerMethodField(method_name="get_marks")
    course = serializers.SerializerMethodField(method_name='get_course')
    class Meta:
        model = Attendance
        fields = ["id", "course", "date","marks"]

    def get_course(self,obj):
        course = obj.course

        return {
            "id": course.id,
            "name": course.name,
        }

    def get_marks(self, obj):
        attendance_name = obj
        attendance=get_object_or_404(Attendance,pk=attendance_name.id)
        marks = Mark.objects.filter(attendance=attendance)
        return CourseMarksSerializer(marks, many=True).data



class CourseMarksSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField(method_name="get_student")
    class Meta:
        model = Mark
        fields = ["student", "attendance", "is_attended"]

    def get_student(self,obj):

        student = obj.student

        return {
            "id": student.id,
            "username": student.user.username,
            "first_name": student.user.first_name,
            "last_name": student.user.last_name,

        }
#
# class CourseProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Course
#         fields = ["id", "name"]

class ProfileSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField(method_name="get_courses")
    request_join = serializers.SerializerMethodField(method_name="request_joins")
    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "image", "email", "birth_date", "address", "phone_number", "courses", "request_join"]

    def get_courses(self, obj):
        courses = Course.objects.filter(teacher__user=obj)
        return [course.name for course in courses]

    def request_joins(self,obj):
        request_joins = JoinRequest.objects.all()
        return [request_join.student.user.username for request_join in request_joins]



