from main.models import UserSay, Course, Teacher, CustomUser, UserRoleEnum
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass



class UserSaySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSay
        fields = ['id', 'user', 'message', 'created_time']



class CourseSerializer(serializers.ModelSerializer):
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
            'teacher'
        ]
class TeacherCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "name",]


class TeacherSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ['id', 'image', 'courses']

    def get_image(self, obj):
        return obj.user.image.url if obj.user.image else None

    def get_courses(self, obj):
        return TeacherCourseSerializer(obj.courses.all(), many=True).data



