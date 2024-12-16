from django.test import TestCase
from django.contrib.auth.hashers import check_password

class PasswordCheckTest(TestCase):
    def test_check_password(self):
        # Shifrlangan parol
        hashed_password = "pbkdf2_sha256$870000$gdKrV5ZXzjQi9Yoakghy0p$fFHmameAoYbusGu6Algw70Rvs+Lkf2gMOOQP8BSMoo4="
        # Asl parol (foydalanuvchi tomonidan kiritilgan deb taxmin qilamiz)
        plain_password = "sizning_parolingiz"

        # Parolni tekshirish
        is_valid = check_password(plain_password, hashed_password)

        # Kutilgan natijani tekshirish
        self.assertTrue(is_valid, "Parol noto'g'ri!")
