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
    CourseStudentAddView,
    join_request_view,
    # payments
    CoursePaymentsView,
    CoursePaymentTakeView,
    CoursePaymentEditView,
    delete_payment,
    # registrations
    signup_view,
    sign_in_view,
    # students
    student_detail_view,
    StudentEditView,
    student_delete_view,
    GroupTasksView,
    attendances_view,
    AttendanceTakeView,
    AttendanceUpdateView,
    GroupTaskEdit,
    StudentTaskTakeView,
    StudentTaskEdit,
    student_delete_task,
    # teachers
    teacher_detail_view,
    teacher_edit_view,
    # profile
    profile_view,
    user_edit_view,
    # feedbacks
    FeedbacksView,
    # 404
    custom_404,
    set_language, delete_task

)
urlpatterns = [
    path('set_language/<str:language_code>/',set_language, name='set_language'),
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
    path('course/<int:course_id>/delete',course_delete_view,name='course_delete'),
    path('course/<int:course_id>/students',course_student_view,name='course_students'),
    path('course/<int:course_id>/student/add',CourseStudentAddView.as_view(),name='course_student_add'),
    path('course/<int:course_id>/join-request',join_request_view,name='join_request'),
#Payments
    path('course/<int:course_id>/payments',CoursePaymentsView.as_view(),name='course_payments'),
    path('course/<int:course_id>/payment-take',CoursePaymentTakeView.as_view(),name='course_pay_take'),
    path('course/<int:course_id>/payment/<int:student_id>/edit',CoursePaymentEditView.as_view(),name='course_payment_edit'),
    path('course/<int:course_id>/payment/<int:student_id>/delete/',delete_payment, name='delete_payment'),
# registration
    path('signup',signup_view,name='signup'),
    path('login/',sign_in_view,name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    #course students
    path('course/<int:course_id>/student/<int:student_id>/detail',student_detail_view,name='student_detail'),
    path('course/<int:course_id>/student/<int:student_id>/task/<int:task_id>/edit',StudentTaskEdit.as_view(),name='student_task_edit'),
    path('course/<int:course_id>/student/<int:student_id>/task/<int:task_id>/delete',student_delete_task,name='student_task_delete'),
    path('course/<int:course_id>/student/<int:student_id>/edit',StudentEditView.as_view(),name='student_edit'),
    path('course/<int:course_id>/student/<int:student_id>/exit',student_delete_view,name='student_delete'),
    path('course/<int:course_id>/tasks',GroupTasksView.as_view(),name='group_tasks'),
    path('course/<int:course_id>/task/<int:task_id>/edit',GroupTaskEdit.as_view(),name="task_edit_delete"),
    path('delete-task/<int:course_id>/<int:task_id>/', delete_task, name='delete_task'),
    path('course/<int:course_id>/student/<int:student_id>/create-task',StudentTaskTakeView.as_view(),name="student_task_take"),
    #attendance
    path('course/<int:course_id>/attendances',attendances_view,name='attendances'),
    path('course/<int:course_id>/attendance-take',AttendanceTakeView.as_view(),name='attendance_take'),
    path('course/<int:course_id>/attendance/<int:attendance_id>/update',AttendanceUpdateView.as_view(),name='attendance_update'),
    #teacher
    path('teacher/<int:teacher_id>/detail',teacher_detail_view,name="teacher_detail"),
    path('teacher-edit',teacher_edit_view,name='teacher_edit'),
    #profile
    path('profile',profile_view,name='profile'),
    path('profile/<int:user_id>/edit',user_edit_view,name='user_edit'),
    #Feedbacks
    path('feedbacks',FeedbacksView.as_view(),name='feedbacks'),
    #404
    path('404',custom_404,name='error'),

]

