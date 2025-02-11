from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import UserSay, Student, Teacher, Owner, Feedback, Course, JoinRequest, CourseStudent, Attendance, Mark, CourseTask, StudentTask, CoursePayment, TeacherPayment
from django.utils import timezone


class ModelTestCase(TestCase):

    def setUp(self):
        # Creating users
        self.admin_user = get_user_model().objects.create_user(
            username='adminuser', password='password', role='ADMIN')
        self.teacher_user = get_user_model().objects.create_user(
            username='teacheruser', password='password', role='TEACHER')
        self.student_user = get_user_model().objects.create_user(
            username='studentuser', password='password', role='STUDENT')

        # Create instances of models related to users
        self.student = Student.objects.create(user=self.student_user)
        self.teacher = Teacher.objects.create(user=self.teacher_user)
        self.owner = Owner.objects.create(user=self.admin_user)

        # Creating a course
        self.course = Course.objects.create(
            name='Mathematics', description='Math Course', price=100, start_time='10:00', end_time='12:00', schedule_days='Monday, Wednesday', teacher=self.teacher)

    def test_user_model(self):
        """Test CustomUser model"""
        user = self.student_user
        self.assertEqual(user.username, 'studentuser')
        self.assertEqual(user.get_role_display(), 'Student')

    def test_user_say(self):
        """Test UserSay model"""
        message = UserSay.objects.create(user=self.student_user, message="Test message")
        self.assertEqual(message.user.username, 'studentuser')
        self.assertEqual(message.message, "Test message")

    def test_student_teacher_owner(self):
        """Test Student, Teacher, and Owner relationships"""
        self.assertEqual(self.student.user.username, 'studentuser')
        self.assertEqual(self.teacher.user.username, 'teacheruser')
        self.assertEqual(self.owner.user.username, 'adminuser')

    def test_feedback_model(self):
        """Test Feedback model"""
        feedback = Feedback.objects.create(user=self.student_user, title="Bug Report", description="A bug found.", page_name="Homepage", type='bug')
        self.assertEqual(feedback.user.username, 'studentuser')
        self.assertEqual(feedback.status, 'new')

    def test_course_model(self):
        """Test Course model"""
        self.assertEqual(self.course.name, 'Mathematics')
        self.assertEqual(self.course.teacher.user.username, 'teacheruser')

    def test_join_request(self):
        """Test JoinRequest model"""
        join_request = JoinRequest.objects.create(student=self.student, course=self.course)
        self.assertEqual(join_request.student.user.username, 'studentuser')
        self.assertEqual(join_request.course.name, 'Mathematics')

    def test_course_student_model(self):
        """Test CourseStudent model"""
        course_student = CourseStudent.objects.create(course=self.course, student=self.student, teacher=self.teacher, start_date=timezone.now())
        self.assertEqual(course_student.course.name, 'Mathematics')
        self.assertEqual(course_student.student.user.username, 'studentuser')
        self.assertEqual(course_student.teacher.user.username, 'teacheruser')

    def test_attendance_model(self):
        """Test Attendance model"""
        attendance = Attendance.objects.create(course=self.course, date=timezone.now().date())
        self.assertEqual(attendance.course.name, 'Mathematics')

    def test_mark_model(self):
        """Test Mark model"""
        attendance = Attendance.objects.create(course=self.course, date=timezone.now().date())
        mark = Mark.objects.create(student=self.student, attendance=attendance, is_attended=True)
        self.assertEqual(mark.student.user.username, 'studentuser')
        self.assertEqual(mark.is_attended, True)

    def test_course_task_model(self):
        """Test CourseTask model"""
        course_task = CourseTask.objects.create(course=self.course, task_name="Homework", definition="Complete the task", given_date=timezone.now().date(), until_date=timezone.now().date(), is_done=False)
        self.assertEqual(course_task.course.name, 'Mathematics')
        self.assertEqual(course_task.task_name, "Homework")

    def test_student_task_model(self):
        """Test StudentTask model"""
        student_task = StudentTask.objects.create(student=self.student, course=self.course, name="Task 1", description="Task description", given_date=timezone.now().date(), until_date=timezone.now().date(), is_done=False)
        self.assertEqual(student_task.student.user.username, 'studentuser')
        self.assertEqual(student_task.is_done, False)

    def test_course_payment_model(self):
        """Test CoursePayment model"""
        course_payment = CoursePayment.objects.create(course=self.course, student=self.student, price=100, pay_date=timezone.now().date(), payment_method="Credit Card", is_paid=True)
        self.assertEqual(course_payment.student.user.username, 'studentuser')
        self.assertEqual(course_payment.is_paid, True)

    def test_teacher_payment_model(self):
        """Test TeacherPayment model"""
        teacher_payment = TeacherPayment.objects.create(teacher=self.teacher, price=200, is_paid=True)
        self.assertEqual(teacher_payment.teacher.user.username, 'teacheruser')
        self.assertEqual(teacher_payment.is_paid, True)

