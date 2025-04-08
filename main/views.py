from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .models import Course, UserSay, CustomUser, Student, Teacher, CourseStudent, CourseTask, Attendance, Mark, \
    JoinRequest, CoursePayment, StudentTask, Feedback, Contact
from .forms import CourseCreateForm, UserSayForm, CustomUserCreationForm, CourseUpdateForm, CourseStudentCreateForm, \
    StudentEditForm, GroupTaskForm, StudentTakeTask, FeedbackForm
from django.views.generic import View,UpdateView
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse,JsonResponse
from datetime import datetime,date
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .decorators import teacher_required

#
from languages import en
from languages import uz


import json



def set_language(request, language_code):
    # Tilni sessiyada saqlash
    request.session['language'] = language_code
    # Foydalanuvchini avvalgi sahifaga yoki asosiy sahifaga qaytarish
    return redirect(request.META.get('HTTP_REFERER', '/'))
# Create your views here

class IndexView(View):
    @method_decorator(login_required)
    def post(self, request):
        form = UserSayForm(request.POST)
        language = request.session.get('language', 'en')

        # Tarjimalarni tanlash
        if language == 'uz':
            translations = uz.index.translations
        else:
            translations = en.index.translations

        if form.is_valid():
            form.save(user=request.user)
            return redirect('index')
        else:
            ctx = {
                'form': form,
                'translations': translations
            }

        return render(request, 'main/index.html', ctx)

    def get(self, request):
        user_says = UserSay.objects.all()
        language = request.session.get('language', 'en')

        # Tarjimalarni tanlash
        if language == 'uz':
            translations = uz.index.translations
        else:
            translations = en.index.translations

        ctx = {
            'user_says': user_says,
            'translations': translations
        }
        return render(request, 'main/index.html', ctx)



def about_view(request):
    language = request.session.get('language', 'en')

    # Tarjimalarni tanlash
    if language == 'uz':
        translations = uz.about.translations
    else:
        translations = en.about.translations

    ctx = {
        'translations': translations
    }
    return render(request, 'main/about.html', ctx)


@login_required()
def contact_view(request):
    if request.method == "POST":
        user_id = request.user.id
        user = CustomUser(id=int(user_id))
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        Contact.objects.create(
            user=user,
            subject=subject,
            message=message
        )

    return render(request, 'main/contact.html')


#Course

class CoursesView(View):
    template_name = 'course/courses.html'

    def get(self, request):
        # if not request.user.is_authenticated:
        #     messages.error(request, "Tizimga kirishingiz kerak.")
        #     return redirect('login')
        if request.user.is_authenticated:

            if request.user.role == "ADMIN":
                # ADMIN uchun barcha kurslar
                course_data = Course.objects.all()
                form = CourseCreateForm()
                language = request.session.get('language', 'en')

                if language == 'uz':
                    translations = uz.courses.translations
                else:
                    translations = en.courses.translations
                ctx = {
                    'course_data': course_data,
                    'form': form,
                    'translations': translations
                }
                return render(request, self.template_name, ctx)

            elif request.user.role == "TEACHER":
                # O'qituvchi faqat o'z kurslarini ko'radi

                teacher_id = Teacher.objects.get(user=request.user.id)
                course_data = Course.objects.filter(teacher=teacher_id)
                course_student = CourseStudent.objects.filter(teacher=request.user.id).exists()
                form = CourseCreateForm()

                language = request.session.get('language', 'en')

                if language == 'uz':
                    translations = uz.courses.translations
                else:
                    translations = en.courses.translations

                ctx = {
                    'course_data': course_data,
                    'form': form,
                    'course_student': course_student,
                    'translations': translations
                }
                return render(request, self.template_name, ctx)

            elif request.user.role == "STUDENT":
                student = request.user
                course_data = Course.objects.all()
                course_student = CourseStudent.objects.get(student=request.user.id)
                form = CourseCreateForm()

                is_join_request = JoinRequest.objects.filter(student=student.id).exists()

                language = request.session.get('language', 'en')

                if language == 'uz':
                    translations = uz.courses.translations
                else:
                    translations = en.courses.translations

                ctx = {
                    'course_data': course_data,
                    'student': student,
                    'form': form,
                    'is_join_request': is_join_request,
                    'course_student': course_student,
                    'translations': translations
                }
                return render(request, self.template_name, ctx)

            else:
                # Boshqa foydalanuvchilar uchun bu sahifani ko'rsatmaslik
                messages.error(request, "Sizda kurslar ro'yxatini ko'rish yoki yaratish huquqi yo'q.")
                return redirect('index')  # Yoki boshqa sahifaga yo'naltirish
        else:
            course_data = Course.objects.all()
            form = CourseCreateForm()
            # is_join_request = JoinRequest.objects.get(student=student).exists()
            language = request.session.get('language', 'en')

            if language == 'uz':
                translations = uz.courses.translations
            else:
                translations = en.courses.translations

            ctx = {
                'course_data': course_data,
                'form': form,
                'translations': translations
                # 'is_join_request': is_join_request

            }
            return render(request, self.template_name, ctx)

    @method_decorator(login_required)
    def post(self, request):
        # Foydalanuvchi tizimga kirganmi?
        if not request.user.is_authenticated:
            messages.error(request, "Kurs yaratish uchun tizimga kirishingiz kerak.")
            return redirect('login')

        form = CourseCreateForm(request.POST, request.FILES)

        if form.is_valid():
            course = form.save(commit=False)

            # Faqat Admin yoki O'qituvchi kurs yaratishi mumkin
            if request.user.role == "TEACHER":
                teacher, created = Teacher.objects.get_or_create(user=request.user)
                course.teacher = teacher
            else:
                messages.error(request, 'Faqat Admin yoki O\'qituvchi kurs yaratishi mumkin.')
                return redirect('courses')

            course.save()
            messages.success(request, 'Kurs muvaffaqiyatli yaratildi!')
            return redirect('courses')
        else:
            messages.error(request, 'Formada xatoliklar mavjud.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

        # Agar form noto'g'ri bo'lsa, kurslarni qayta yuklab va formni ko'rsatamiz
        course_data = Course.objects.all()
        language = request.session.get('language', 'en')

        if language == 'uz':
            translations = uz.courses.translations
        else:
            translations = en.courses.translations

        ctx = {
            'form': form,
            'course_data': course_data,
            'translations': translations
        }
        return render(request, self.template_name, ctx)

@teacher_required
def course_update_view(request, pk):
    course = get_object_or_404(Course, pk=pk)

    form = CourseUpdateForm(request.POST, instance=course)

    if request.method == "POST":
        form = CourseUpdateForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses')  # Kurslar ro'yxati sahifasiga yo'naltirish
        else:
            return HttpResponse("Forma validatsiyadan o'tmagan")
    else:
        form = CourseUpdateForm(instance=course)

    ctx = {
        'course': course,
        'form': form,
    }

    return render(request, 'course/course_edit.html', ctx)


def course_delete_view(request, course_id):
    if request.method == 'POST':
        # Ma'lumotni olish va o‘chirish
        course = Course.objects.get(id=course_id)
        if course:
            course.delete()
            success_url = reverse('courses')
            return JsonResponse({'redirect_url': success_url})

    return JsonResponse({'error': 'Xatolik yuz berdi'}, status=400)


def course_student_view(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    course_students = CourseStudent.objects.filter(course=course.id)

    ctx = {
        'course': course,
        'course_students': course_students,
    }
    return render(request, 'course/course_students.html', ctx)

class CourseStudentAddView(View):

    def get(self,request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        students = JoinRequest.objects.filter(course=course.id)

        ctx = {
            'course': course,
            'students': students
        }
        return render(request, 'course/course_student_add.html', ctx)


    def post(self,request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        students = JoinRequest.objects.filter(course=course.id)
        if request.user.role == "TEACHER":
            try:
                teacher = Teacher.objects.get(user=request.user.id)
                student_id = request.POST.get('student')
                student = Student.objects.filter(id=student_id).first()


                start_date = request.POST.get('start_date')

                if not start_date:
                    return HttpResponse("Boshlanish sanasi kiritilmagan!", status=400)

                new_student = CourseStudent.objects.create(
                    course=course,
                    student=student,
                    teacher=teacher,
                    start_date=start_date
                )
                JoinRequest.objects.get(course=course_id,student=student_id).delete()
                marks = Mark.objects.filter(attendance__course=course).all()
                if marks:
                    for mark in marks:
                        if new_student == mark.student:
                            Mark.objects.create(student=new_student,is_attended=-1)
                        else:
                            pass
                else:
                    pass

                return redirect('course_students', course_id=course.id)

            except Teacher.DoesNotExist:
                return HttpResponse("O'qituvchi topilmadi. Iltimos, tizimga to'g'ri ma'lumot bilan kiring.", status=404)



        ctx = {
            'course': course,
            'students': students
        }
        return render(request, 'course/course_student_add.html', ctx)


def gallery_view(request):
    return render(request, 'main/gallery.html')


def single_view(request):
    return render(request, 'main/single.html')


def blogs_view(request):
    return render(request, 'main/blog.html')


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.save()

            # filter yordamida faqat bitta studentni olish
            student = Student.objects.filter(user=user).first()  # Birinchi studentni olish

            if not student:
                # Agar student mavjud bo'lmasa, yangi yaratamiz
                Student.objects.create(user=user)

            login(request, user)  # Foydalanuvchini tizimga kiritamiz
            return redirect('index')  # Bosh sahifaga yo'naltirish
        else:
            # Agar xatolik bo'lsa, u xatolikni foydalanuvchiga ko'rsatamiz
            # print(form.errors)
            pass
    else:
        form = CustomUserCreationForm()

    return render(request, 'registrations/sign_up.html', {'form': form})


def sign_in_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Foydalanuvchini tizimga kiritamiz
                return redirect('index')  # Bosh sahifaga yo'naltirish
            else:
                messages.error(request, "Foydalanuvchi nomi yoki parol noto‘g‘ri")
        else:
            messages.error(request, "Foydalanuvchi nomi yoki parol noto‘g‘ri")
    else:
        form = AuthenticationForm()

    return render(request, 'registrations/sign_in.html', {'form': form})


def logout_view(request):
    logout(request)  # Foydalanuvchini tizimdan chiqarish
    return redirect('index')


class StudentEditView(View):
    def get(self,request, course_id, student_id):
        course_student = CourseStudent.objects.get(course=course_id, student=student_id)
        student = course_student.student.user
        form = StudentEditForm(instance=student)

        ctx = {
            'form': form,
            'course_student': course_student,
            'student': student,
        }
        return render(request, 'student/student_edit.html', ctx)
    def post(self,request, course_id, student_id):
        course_student = CourseStudent.objects.get(course=course_id, student=student_id)
        student = course_student.student.user

        if request.method == "POST":
            form = StudentEditForm(request.POST, request.FILES, instance=student)
            if form.is_valid():
                form.save()
                return redirect('student_detail', course_id=course_id, student_id=student_id)
        else:
            form = StudentEditForm(instance=student)

        # Har bir sharoit uchun HttpResponse qaytarilishi ta'minlanadi
        ctx = {
            'form': form,
            'course_student': course_student,
            'student': student,
        }
        return render(request, 'student/student_edit.html', ctx)


def student_delete_view(request, course_id, student_id):
    if request.method == 'POST':
        # Ma'lumotni olish va o‘chirish
        course_payment = CourseStudent.objects.filter(course_id=course_id, student_id=student_id).first()
        if course_payment:
            course_payment.delete()


            success_url = reverse('course_students', kwargs={'course_id': course_id})
            return JsonResponse({'redirect_url': success_url})

    return JsonResponse({'error': 'Xatolik yuz berdi'}, status=400)


#Student Task
class StudentTaskTakeView(View):
    def post(self,request, course_id, student_id):
        today = timezone.now().date()
        course_student = CourseStudent.objects.get(course=course_id, student=student_id)
        if request.method == 'POST':
            # if form.is_valid():
            name = request.POST.get('name')
            description = request.POST.get('description')
            until_date = request.POST.get('until_date')
            StudentTask.objects.create(
                course=course_student.course,
                student=course_student.student,
                name=name,
                description=description,
                given_date=today,
                until_date=until_date,

            )
            return redirect("student_detail", course_id=course_id, student_id=student_id)
        else:
            pass

        ctx = {
            'course_student': course_student,
            'today': today,
            'course_id': course_id,
            'student_id': student_id
        }
        return render(request, 'student/student_task_take.html', ctx)

    def get(self,request, course_id, student_id):
        today = timezone.now().date()
        course_student = CourseStudent.objects.get(course=course_id, student=student_id)

        ctx = {
            'course_student': course_student,
            'today': today,
            'course_id': course_id,
            'student_id': student_id
        }
        return render(request, 'student/student_task_take.html', ctx)

class StudentTaskEdit(View):
    def get(self,request,course_id,student_id,task_id):
        student_task = StudentTask.objects.get(id=task_id,course=course_id,student=student_id)
        ctx = {
            'student_task': student_task
        }
        return render(request,'student/student_task_edit.html',ctx)

    def post(self, request, course_id, student_id,task_id):
        if request.method == "POST":
            name = request.POST.get('name')
            description = request.POST.get('description')
            given_date_str = request.POST.get('given_date')
            until_date_str = request.POST.get('until_date')
            given_date = datetime.strptime(given_date_str, "%Y-%m-%d").date()
            until_date = datetime.strptime(until_date_str, "%Y-%m-%d").date()
            is_done = request.POST.get('is_done') == "on"

            StudentTask.objects.filter(id=task_id,course=course_id,student=student_id).update(
                course=course_id,
                student=student_id,
                name=name,
                description=description,
                until_date=until_date,
                given_date=given_date,
                is_done=is_done
            )
            return redirect('student_detail', course_id=course_id, student_id=student_id)

        return render(request, 'student/student_task_edit.html')

def student_delete_task(request, course_id, student_id,task_id):
    student_task = StudentTask.objects.filter(id=task_id,course=course_id,student=student_id).first()
    print(student_task)

    if request.method == 'POST':
        student_task.delete()

        success_url = reverse('student_detail', kwargs={'course_id': course_id, 'student_id':student_id})
        return JsonResponse({'redirect_url': success_url})


    return JsonResponse({'error': 'Xatolik yuz berdi'}, status=400)


def student_detail_view(request, course_id, student_id):
    course_student = CourseStudent.objects.get(course=course_id, student=student_id)
    student = course_student.student
    student_tasks = StudentTask.objects.filter(student=student)



    ctx = {
        'course_student': course_student,
        'student': student,
        'student_tasks': student_tasks
    }
    return render(request, 'student/student_detail.html', ctx)

class GroupTasksView(View):
    def get(self,request, course_id):
        course = course_id
        course_data = Course.objects.get(id=course_id)
        course_tasks = CourseTask.objects.filter(course=course_id).all()
        today = timezone.now().date()
        language = request.session.get('language', 'en')

        if language == 'uz':
            translations = uz.group_task.translations
        else:
            translations = en.group_task.translations


        ctx = {
            'course_data': course_data,
            'course_tasks': course_tasks,
            'translations': translations,
            'today': today
        }
        return render(request, 'course/group_tasks.html', ctx)
    def post(self,request,course_id):
        # Fetch the course related to the student
        course = course_id
        course_data = Course.objects.get(id=course_id)
        course_tasks = CourseTask.objects.filter(course=course_id).all()
        today = timezone.now().date()

        if request.method == "POST":
            form = GroupTaskForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('group_tasks', course_id)
            else:
                # print(form.errors)
                pass
        else:
            form = GroupTaskForm()

        language = request.session.get('language', 'en')

        if language == 'uz':
            translations = uz.create_group_task.translations
        else:
            translations = en.create_group_task.translations

        ctx = {
            'course_tasks': course_tasks,
            'course': course,
            'course_data': course_data,
            'form': form,
            'today': today,
            'translations': translations
        }

        return render(request, 'course/group_tasks.html', ctx)


class GroupTaskEdit(View):
    def get(self,request,course_id,task_id):
        course = Course.objects.get(id=course_id)
        task = CourseTask.objects.get(id=task_id)
        today = timezone.now().date()



        ctx = {
            'course': course,
            'task': task,
            'today': today
        }
        return render(request,'course/task_edit.html',ctx)

    def post(self,request,course_id,task_id):
        course = Course.objects.get(id=course_id)
        task = CourseTask.objects.get(id=task_id)
        today = timezone.now().date()

        if request.method == "POST":
            task_name = request.POST.get('task_name')
            definition = request.POST.get('definition')
            given_date = request.POST.get('given_date')
            until_date = request.POST.get('until_date')
            is_done = request.POST.get('is_done') == 'on'

            CourseTask.objects.filter(id=task.id).update(course=course,
                                                     task_name=task_name,
                                                     definition=definition,
                                                     given_date=given_date,
                                                     until_date=until_date,
                                                     is_done=is_done)
            return redirect('group_tasks', course_id=course.id)



        ctx = {
            'course': course,
            'task': task,
            'today': today
        }
        return  render(request,'course/task_edit.html',ctx)


def delete_task(request, course_id, task_id):
    course = get_object_or_404(Course, id=course_id)
    task = get_object_or_404(CourseTask, id=task_id)

    if request.method == 'POST':
        task.delete()  # Taskni o'chirish
        return redirect('group_tasks', course_id=course.id)
    else:
        return redirect('group_tasks', course_id=course.id)

def attendances_view(request, course_id):
    today = timezone.now().date()
    course = get_object_or_404(Course, id=course_id)
    course_students = CourseStudent.objects.filter(course=course_id)
    attendances = Attendance.objects.filter(course=course_id).all()
    # attendance  = Attendance.objects.filter(course=course_id).first()
    marks = Mark.objects.filter(attendance__in=attendances)

    is_att_taken = Attendance.objects.filter(date=today, course=course_id).exists()
    date_list = Attendance.objects.filter(course=course_id).order_by('date')
    date_paginator = Paginator(date_list, 2)  # Show 5 dates per page
    date_page = request.GET.get('date_page')

    try:
        attendances_paginated = date_paginator.page(date_page)
    except PageNotAnInteger:
        attendances_paginated = date_paginator.page(1)
    except EmptyPage:
        attendances_paginated = date_paginator.page(date_paginator.num_pages)

    paginated_dates = attendances_paginated.object_list

    students_with_marks = []

    for course_student in course_students:
        for attendance in attendances:
            # print(attendance)
            marks_for_paginated_dates = [
                Mark.objects.filter(attendance=attendance, student=course_student.student).first()
                for attendance in paginated_dates
            ]
        try:
            students_with_marks.append({
                'student': course_student.student,
                'marks': marks_for_paginated_dates
            })
        except:
            pass

    # return HttpResponse(students_with_marks)
    # print(students_with_marks)

    paginator = Paginator(students_with_marks, 14)  # Show 10 students per page
    page = request.GET.get('page')
    try:
        students_with_marks_paginated = paginator.page(page)
    except PageNotAnInteger:
        students_with_marks_paginated = paginator.page(1)
    except EmptyPage:
        students_with_marks_paginated = paginator.page(paginator.num_pages)

    language = request.session.get('language', 'en')

    if language == 'uz':
        translations = uz.attendances.translations
    else:
        translations = en.attendances.translations

    ctx = {
        'course': course,
        'course_students': course_students,
        'attendances': attendances,
        'marks': marks,
        'students_with_marks': students_with_marks,
        'date_paginator': date_paginator,
        'date_page_obj': attendances_paginated,
        'paginated_dates': paginated_dates,
        'today': today,
        # 'attendance': attendance,
        'is_att_taken': is_att_taken,
        'translations': translations
    }

    return render(request, 'attendances/attendances.html', ctx)


# attendance
class AttendanceTakeView(View):
    def post(self, request, course_id):
        today = timezone.now().date()
        course = get_object_or_404(Course, id=course_id)
        course_students = CourseStudent.objects.filter(course=course)

        if request.method == "POST":
            today = timezone.now().date()
            course = get_object_or_404(Course, id=course_id)
            course_students = CourseStudent.objects.filter(course=course)
            # print(request.method)

            attendance = Attendance.objects.create(course=course, date=today)
            for course_student in course_students:
                # print(course_student.student.id)
                # print(course_student.student.user.username)
                attendance_key = f"attended_{course_student.student.id}"
                is_attended = request.POST.get(attendance_key) == 'on'
                # print(f"Attendance key: {attendance_key}, Is attended: {is_attended}")

                mark = Mark.objects.create(
                    student=course_student.student,
                    attendance=attendance,
                    is_attended=is_attended
                )
                # print(f"Mark created: {mark}")
            return redirect('attendances', course.id)

        ctx = {
            'course': course,
            # 'attendance': attendance
            'course_students': course_students,
            'today': today,

        }

        return render(request, 'attendances/attendance_take.html', ctx)

    def get(self, request, course_id):
        today = timezone.now().date()
        course = get_object_or_404(Course, id=course_id)
        course_students = CourseStudent.objects.filter(course=course)


        ctx = {
            'course': course,
            'course_students': course_students,
            'today': today,

        }

        return render(request, 'attendances/attendance_take.html', ctx)


class AttendanceUpdateView(View):
    def get(self, request, course_id, attendance_id):
        course_id = course_id
        attendance = Attendance.objects.get(id=attendance_id)
        today = datetime.now().date()
        marks = Mark.objects.filter(attendance=attendance)

        language = request.session.get('language', 'en')

        if language == 'uz':
            translations = uz.attendance_update.translations
        else:
            translations = en.attendance_update.translations

        ctx = {
            'attendance': attendance,
            'marks': marks,
            'course_id': course_id,
            'translations': translations
        }

        return render(request, 'attendances/attendance_update.html', ctx)

    def post(self, request, course_id, attendance_id):
        course_id = course_id
        attendance = Attendance.objects.get(id=attendance_id)
        marks = Mark.objects.filter(attendance=attendance)
        today = datetime.now().date()

        if attendance.date == today:
            if request.method == "POST":
                for mark in marks:
                    is_attended_input = request.POST.get(f"is_attended_{mark.id}")
                    mark.is_attended = is_attended_input == 'on'
                Mark.objects.bulk_update(marks, ['is_attended'])
                return redirect('attendances', course_id=course_id)

            language = request.session.get('language', 'en')

            if language == 'uz':
                translations = uz.attendance_update.translations
            else:
                translations = en.attendance_update.translations

            ctx = {
                'attendance': attendance,
                'marks': marks,
                'course_id': course_id,
                'translations': translations
            }

            return render(request, 'attendances/attendance_update.html', ctx)
        else:
            return HttpResponse("Faqat bugungi sanadagi davomaladlarni yangilash mumkin")


#Teacher
def teacher_edit_view(request):
    return render(request, 'teacher/teacher_edit.html')


@login_required
def teachers_view(request):
    # only_admin = request.user.role == 'ADMIN'
    user = request.user
    if user.role == "ADMIN":

        teachers = Teacher.objects.all()

        teacher_courses = []
        for teacher in teachers:
            course = Course.objects.filter(teacher=teacher)
            teacher_courses.append(
                {
                    'teacher': teacher,
                    'course': course
                }
            )
        # print(teacher_courses)

        ctx = {
            'teachers': teachers,
            # 'course': courses,
            'teacher_courses': teacher_courses
        }

        return render(request, 'teacher/teachers.html', ctx)

    elif user.role == "TEACHER":
        teacher = Teacher.objects.get(user=user.id)
        courses = Course.objects.filter(teacher=teacher)

        # teachers = Teacher.objects.all()
        ctx = {
            'teacher': teacher,
            'courses': courses
        }

        return render(request, 'teacher/teachers.html', ctx)


    elif user.role == "STUDENT":
        student = Student.objects.get(user=request.user)
        teachers = CourseStudent.objects.filter(student=student)
        teacher_courses = []
        for teacher in teachers:
            course = Course.objects.filter(teacher=teacher.teacher)
            teacher_courses.append(
                {
                    'teacher': teacher.teacher,
                    'course': course
                }
            )
        # print(teacher_courses)
        # print(teacher_courses)

        ctx = {
            'teachers': teachers,
            # 'course': courses,
            'teacher_courses': teacher_courses
        }

        return render(request, 'teacher/teachers.html', ctx)


def teacher_detail_view(request, teacher_id):
    teacher = Teacher.objects.filter(user=teacher_id).first()

    courses = Course.objects.filter(teacher=teacher)

    ctx = {
        'teacher': teacher,
        'courses': courses
    }
    return render(request, 'teacher/teacher_detail.html', ctx)


@login_required
def profile_view(request):
    join_requests = JoinRequest.objects.filter(joinded=False)
    user = request.user


    if user.role == "TEACHER" or user.role == "ADMIN":
        teacher = Teacher.objects.get(user=user)
        courses = Course.objects.filter(teacher=teacher)
        course_students = CourseStudent.objects.filter(teacher=teacher)

        # student = JoinRequest.objects.all()
        number = 0
        for course_student in course_students:
            JoinRequest.objects.filter(student=course_student.student).update(joinded=True)
            number += 1
        # print(join_requests)
        ctx = {
            'join_requests': join_requests,
            'user': user,
            'courses': courses,
            'course_students': course_students,
            'number': number
        }
        return render(request, 'main/profile.html', ctx)

    elif user.role == "STUDENT":
        student = Student.objects.get(user=user)
        course_exists = CourseStudent.objects.filter(student=student).exists()
        if course_exists:
            course = CourseStudent.objects.get(student=student)
            student_tasks = StudentTask.objects.filter(student=student)
            course_payments = CoursePayment.objects.filter(course=course.course, student=student)
            ctx = {
                'join_requests': join_requests,
                'user': user,
                'student': student,
                'course': course,
                'student_tasks': student_tasks,
                'course_payments': course_payments
            }
            return render(request, 'main/profile.html', ctx)
        else:

            ctx = {
                'join_requests': join_requests,
                'user': user,
                'student': student,

            }
            return render(request, 'main/profile.html', ctx)


def user_edit_view(request, user_id):
    user = CustomUser.objects.get(id=user_id)

    if request.method == "POST":
        form = StudentEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = StudentEditForm(instance=user)

    ctx = {
        'form': form,
    }
    return render(request, 'main/user_edit.html', ctx)





def join_request_view(request, course_id):
    course = Course.objects.get(id=course_id)
    user = request.user
    student = Student.objects.get(id=user.id)

    # print(is_join_request)
    # if is_join_request:
    join_request = JoinRequest.objects.create(
        student=student,
        course=course,
        is_sent=True
    )
    # is_join_request = JoinRequest.objects.get(student=student).exists()
    language = request.session.get('language', 'en')

    if language == 'uz':
        translations = uz.join_request.translations
    else:
        translations = en.join_request.translations

    ctx = {
        "course": course,
        'translations':translations
    }
    return render(request, 'course/join_request.html', ctx)
    # else:
    #     return HttpResponse("Siz course ga so'rov yuborgansiz iltimos kuting")


#Payemnts


class CoursePaymentTakeView(View):
    def get(self, request, course_id):
        today = timezone.now().date()
        course = Course.objects.get(id=course_id)
        students = CourseStudent.objects.filter(course=course_id)

        ctx = {
            # 'student': student,
            'students': students,
            'course': course,
            'today': today


        }

        return render(request, 'payments/course_pay_take.html', ctx)
        # else:
        #
        #     return HttpResponse("Post method emas")

    def post(self, request, course_id):
        today = timezone.now().date()
        # print(today)
        course = CourseStudent.objects.get(id=course_id)
        students = CourseStudent.objects.filter(course=course_id)

        student = request.POST.get('student')
        price = request.POST.get('price')
        payment_method = request.POST.get('payment_method')
        is_paid = request.POST.get('is_paid') == "on"

        student = get_object_or_404(Student, id=student)
        if request.POST:
            # CoursePayment yaratish
            CoursePayment.objects.create(
                course=course.course,
                student=student,
                price=float(price),
                pay_date=today,
                payment_method=payment_method,
                is_paid=is_paid,
            )

            return redirect('course_payments', course_id)

        ctx = {
            'students': students,
            'course': course,
            'today': today

        }

        return render(request, 'payments/course_pay_take.html', ctx)
    # else:
    #
    #     return HttpResponse("Post method emas")


class CoursePaymentsView(View):
    def get(self, request, course_id):
        course_payments = CoursePayment.objects.filter(course=course_id)
        course = get_object_or_404(Course, id=course_id)

        ctx = {
            'course_payments': course_payments,
            'course': course
        }
        return render(request, 'payments/course_payments.html', ctx)

def delete_payment(request, course_id, student_id):
    if request.method == 'POST':
        course_payment = CoursePayment.objects.filter(course=course_id, student=student_id).first()
        course_payment.delete()
        return redirect('course_payments',course_id=course_id)

    return JsonResponse({'success': False}, status=400)



class CoursePaymentEditView(View):
    def get(self, request, course_id, student_id):
        course_payment = get_object_or_404(CoursePayment, course=course_id, student=student_id)

        ctx = {
            'course_payment': course_payment,
        }
        return render(request, 'payments/course_payment_edit.html', ctx)

    def post(self, request, course_id, student_id):
        course_student = CourseStudent.objects.get(course=course_id,student=student_id)
        if request.method == 'POST':
            price = request.POST.get('price')
            payment_method = request.POST.get('payment_method')
            pay_date_str = request.POST.get('pay_date')# "2025-02-07"
            pay_date = datetime.strptime(pay_date_str, "%Y-%m-%d").date()
            is_paid = request.POST.get('is_paid') == "on"


            course_payment = get_object_or_404(CoursePayment, course=course_id, student=student_id)

            course_payment.course = course_student.course
            course_payment.student = course_student.student
            course_payment.price = float(price)
            course_payment.payment_method = payment_method
            course_payment.pay_date = pay_date
            course_payment.is_paid = is_paid
            course_payment.save()

            return redirect("course_payments", course_id=course_id)  # Muvaffaqiyatli yangilansa, sahifani yangilash

        return HttpResponse("Invalid request", status=400)


def change_user_role(request, user_id, new_role):
    user = get_object_or_404(CustomUser, id=user_id)
    user.role = new_role
    user.save()  # Signal avtomatik ravishda ishlaydi
    return redirect('user_list')


class FeedbacksView(LoginRequiredMixin,View):
    def get(self,request):
        user = get_object_or_404(CustomUser,pk=request.user.id)
        is_sended = Feedback.objects.filter(user=user).first()
        type_feedbacks = Feedback.FEEDBACK_TYPES

        feedbacks = Feedback.objects.all()

        ctx = {

            'feedbacks': feedbacks,
            'user': user,
            'type_feedbacks': type_feedbacks,
            'is_sended':is_sended
        }
        return render(request,'main/feedbacks.html',ctx)

    def post(self, request):
        # Foydalanuvchini olish
        user = get_object_or_404(CustomUser, pk=request.user.id)
        # print(user)
        feedbacks = Feedback.objects.all()
        title = request.POST.get('title')
        description = request.POST.get('description')
        type = request.POST.get('type')
        page_name = request.POST.get('page_name', 'Default Page')


        if request.method == "POST":


            valid_types = [choice[0] for choice in Feedback.FEEDBACK_TYPES]  # TYPE_CHOICES dan qiymatlar
            if type not in valid_types:
                return JsonResponse({"error": "Invalid type value"}, status=400)


            try:
                Feedback.objects.create(
                    user=user,
                    title=title,
                    description=description,
                    type=type,
                    page_name=page_name,
                    is_send=True
                )
                # return JsonResponse({"success": "Feedback created successfully"})
                return redirect('feedbacks')
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)



        ctx = {

            'user': user,
            'feedbacks': feedbacks,
        }




        return render(request,'main/feedbacks.html',ctx)


def custom_404(request, exception):
    return render(request, '404.html', status=404)
