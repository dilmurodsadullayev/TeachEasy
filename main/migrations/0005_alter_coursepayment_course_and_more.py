# Generated by Django 5.1.2 on 2024-12-18 11:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_joinrequest_joinded"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coursepayment",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="main.course"
            ),
        ),
        migrations.AlterField(
            model_name="coursepayment",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payments",
                to="main.student",
            ),
        ),
    ]
