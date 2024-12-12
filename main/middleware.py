# # middleware.py
# from django.shortcuts import redirect
# from django.urls import reverse
#
#
# class RoleBasedAccessMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         # Har bir so'rovni qayta ishlash
#         user = request.user
#
#         # Foydalanuvchi rolini tekshirish
#         if user.is_authenticated:
#             if user.role == 'student':
#                 # Talabalar faqat "student-dashboard" sahifasiga kirishlari mumkin
#                 if request.path != reverse('student-dashboard'):
#                     return redirect('student-dashboard')
#             elif user.role == 'teacher':
#                 # O'qituvchilar faqat "teacher-dashboard" sahifasiga kirishlari mumkin
#                 if request.path != reverse('teacher-dashboard'):
#                     return redirect('teacher-dashboard')
#             elif user.role == 'admin':
#                 # Adminlar uchun cheklovlar yo'q
#                 pass
#         else:
#             # Foydalanuvchi autentifikatsiya qilinmagan bo'lsa, kirish sahifasiga yo'naltirish
#             return redirect('login')
#
#         response = self.get_response(request)
#         return response
