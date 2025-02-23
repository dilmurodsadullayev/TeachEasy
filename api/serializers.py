from main.models import UserSay, Course, Teacher,CustomUser
from rest_framework import serializers


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

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'birth_date',
            'address',
            'phone_number',
            'role',
            'image'

        ]
