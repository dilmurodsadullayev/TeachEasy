from django.db import models
import datetime
import phonenumbers
from django.db.models import URLField
from phonenumber_field.modelfields import PhoneNumberField
from enum import Enum
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser



class UserRoleEnum(Enum):
    ADMIN = 'Admin'
    TEACHER = 'Teacher'
    STUDENT = 'Student'

    @classmethod
    def choices(cls):
        return [(role.name, role.value) for role in cls]

class CustomUser(AbstractUser):
    birth_date = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True)
    phone_number = PhoneNumberField(unique=True, blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=UserRoleEnum.choices(),
        default=UserRoleEnum.STUDENT.name
    )
    image = models.ImageField(upload_to='users/', blank=True, null=True)

    
    def __str__(self):
        return self.get_full_name() or self.username

    def get_role_display(self):
        return UserRoleEnum[self.role].value

    def clean(self):
        super().clean()
        if self.role not in UserRoleEnum.__members__:
            raise ValidationError({'role': 'Invalid role specified.'})

    def is_admin(self):
        return self.role == UserRoleEnum.ADMIN.name

    def is_teacher(self):
        return self.role == UserRoleEnum.TEACHER.name

    def is_student(self):
        return self.role == UserRoleEnum.STUDENT.name

class UserSay(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='user_says')
    message = models.CharField(max_length=150)
    created_time = models.DateTimeField(auto_now_add=True)  # Yangi nom bilan yangilangan



    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}: {self.message}"
        
    
class Student(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Owner(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# class OwnerCourse(models.Model):
#     own = models.ForeignKey()



class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='courses/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.TimeField()
    end_time = models.TimeField()  
    schedule_days = models.CharField(max_length=70)  
    teacher = models.ForeignKey(Teacher,on_delete=models.SET_NULL,null=True)


    def __str__(self):
        return self.name


class CourseStudent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='course_students')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='course_teachers')
    start_date = models.DateField()

    def __str__(self):
        return f"{self.course.name} - {self.student}"


class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{str(self.course.name)} - {self.date}"


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    is_attended = models.BooleanField(default=False)  # is_attendent o'rniga is_attended

    def __str__(self):

        return f"{self.student} - {str(self.is_attended)}"




class CourseTask(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=50)
    definition = models.TextField()
    given_date = models.DateField()
    until_date = models.DateField()
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course.name} - {self.name}"


class StudentTask(models.Model):
    student = models.ForeignKey(CourseStudent, on_delete=models.CASCADE, related_name='student_tasks')
    course = models.ForeignKey(CourseStudent, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    given_date = models.DateField()
    until_date = models.DateField()
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course.name} - {self.name} {self.is_done}"


class CoursePayment(models.Model):
    course = models.ForeignKey(CourseStudent, on_delete=models.CASCADE)
    student = models.ForeignKey(CourseStudent, on_delete=models.CASCADE, related_name='payments')
    price = models.FloatField()
    pay_date = models.DateField()
    payment_method = models.CharField(max_length=20)  # Bu yerga tanlov qo'shishingiz mumkin
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course.name} - {self.student} {self.is_paid}"



class TeacherPayment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_payments')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='teacher_payments/')
    is_paid = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher.name} - {self.price}"



