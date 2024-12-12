from django.conf.urls.i18n import urlpatterns
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    IndexView,
    about_view,
    contact_view,
    teachers_view,
    gallery_view,
    single_view,
    blogs_view,
# course
    CoursesView,
    course_update_view,
    course_delete_view,
    course_student_view,
    course_student_add_view,
    # registrations
    signup_view,
    sign_in_view,
#students
    student_detail_view,
    student_edit_view,
    student_delete_view,
    group_tasks_view,
    attendances_view,
    AttendanceTakeView,
    AttendanceUpdateView,
    create_group_task_view,
#teachers
    teacher_detail_view,
    teacher_edit_view,
    #profile
    profile_view,
    #404
    error_404_view

)
urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path('about',about_view,name='about'),
    path('contact',contact_view,name='contact'),
    path('teachers',teachers_view,name='teachers'),
    path('gallery',gallery_view,name='gallery'),
    path('single',single_view,name='single'),
    path('blogs',blogs_view,name='blogs'),
    #course
    path('courses',CoursesView.as_view(),name='courses'),
    path('course/<int:pk>/edit',course_update_view,name='course_edit'),
    path('course/<int:pk>/delete',course_delete_view,name='course_delete'),
    path('course/<int:course_id>/students',course_student_view,name='course_students'),
    path('course/<int:course_id>/student/add',course_student_add_view,name='course_student_add'),
    # registration
    path('signup',signup_view,name='signup'),
    path('login/',sign_in_view,name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    #students
    path('course/<int:course_id>/student/<int:student_id>/detail',student_detail_view,name='student_detail'),
    path('course/<int:course_id>/student/<int:student_id>/edit',student_edit_view,name='student_edit'),
    path('course/<int:course_id>/student/<int:student_id>/delete',student_delete_view,name='student_delete'),
    path('course/<int:course_id>/tasks',group_tasks_view,name='group_tasks'),
    path('course/<int:course_id>/create/task',create_group_task_view,name="create_group_task"),
    #attendance
    path('course/<int:course_id>/attendances',attendances_view,name='attendances'),
    path('course/<int:course_id>/attendance-take',AttendanceTakeView.as_view(),name='attendance_take'),
    path('course/<int:course_id>/attendance/<int:attendance_id>/update',AttendanceUpdateView.as_view(),name='attendance_update'),
    #teacher
    path('teacher/<int:teacher_id>/detail',teacher_detail_view,name="teacher_detail"),
    path('teacher-edit',teacher_edit_view,name='teacher_edit'),
    #profile
    path('profile',profile_view,name='profile'),
    #404
    path('404',error_404_view,name='error'),

]

