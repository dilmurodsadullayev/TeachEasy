# Generated by Django 5.1.2 on 2024-12-18 11:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0005_alter_coursepayment_course_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coursepayment",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="main.student"
            ),
        ),
    ]
