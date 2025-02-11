from django.http import HttpResponseForbidden, HttpResponse
from functools import wraps

# Umumiy tekshirish funksiyasi
def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role != role:  # Role tekshirish
                return HttpResponseForbidden(f"Siz {role} ro'li uchun ruxsatga ega emassiz.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def teacher_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        print(f"Foydalanuvchi: {request.user}, Ro'l: {getattr(request.user, 'role', None)}")
        if not request.user.is_authenticated or request.user.role != 'TEACHER':
            return HttpResponseForbidden("Sizda bu amalni bajarishga ruxsat yo'q.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# Maxsus decoratorlar
def owner_required(view_func):
    return role_required('Owner')(view_func)

# def teacher_required(view_func):
#     return role_required('Teacher')(view_func)

def student_required(view_func):
    return role_required('Student')(view_func)
