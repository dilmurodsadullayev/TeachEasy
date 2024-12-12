from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Student, Teacher, Owner
from .models import UserRoleEnum

@receiver(post_save, sender=CustomUser)
def handle_role_change(sender, instance, **kwargs):
    """
    Foydalanuvchining role maydoni o'zgartirilganda, tegishli jadvalni yangilaydi.
    """

    # Foydalanuvchi rolini tekshiramiz
    if instance.role == UserRoleEnum.TEACHER.name:
        # Agar foydalanuvchi Teacher roliga o'tgan bo'lsa
        # Student jadvalida mavjud bo'lsa, o'chirib tashlash
        Student.objects.filter(user=instance).delete()

        # Teacher jadvalida mavjud bo'lmasa, qo'shish
        Teacher.objects.get_or_create(user=instance)

    elif instance.role == UserRoleEnum.STUDENT.name:
        # Agar foydalanuvchi Student roliga o'tgan bo'lsa
        # Teacher jadvalida mavjud bo'lsa, o'chirib tashlash
        Teacher.objects.filter(user=instance).delete()

        # Student jadvalida mavjud bo'lmasa, qo'shish
        Student.objects.get_or_create(user=instance)

    elif instance.role == UserRoleEnum.ADMIN.name:
        # Agar foydalanuvchi ADMIN roliga o'tgan bo'lsa
        # Teacher va Student jadvallaridan o'chirish
        Teacher.objects.filter(user=instance).delete()
        Student.objects.filter(user=instance).delete()

        # Admin (Owner) jadvalida mavjud bo'lmasa, qo'shish
        Owner.objects.get_or_create(user=instance)

    else:
        # Agar role hech biriga mos kelmasa, barcha jadvallardan o'chirish
        Teacher.objects.filter(user=instance).delete()
        Student.objects.filter(user=instance).delete()
        Owner.objects.filter(user=instance).delete()
