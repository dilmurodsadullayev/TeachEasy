from django.contrib import admin
from .models import (
    CustomUser,
    Course,
    CourseStudent,
    Attendance,
    Mark,
    CourseTask,
    StudentTask,
    CoursePayment,
    TeacherPayment,
    UserSay,
    Teacher,
    Student,
    Owner

)
# Register your models here.
class UserSayAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_time') 


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'get_role_display', 'email', 'birth_date', 'phone_number']
    search_fields = ['username', 'email']
    list_filter = ['role']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'birth_date', 'address', 'phone_number', 'image')}),
        ('Permissions', {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Course)
admin.site.register(CourseStudent)
admin.site.register(Attendance)
admin.site.register(Mark)
admin.site.register(CourseTask)
admin.site.register(StudentTask)
admin.site.register(CoursePayment)
admin.site.register(TeacherPayment)
admin.site.register(UserSay,UserSayAdmin)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Owner)



