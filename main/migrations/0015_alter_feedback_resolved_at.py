# Generated by Django 5.1.2 on 2025-02-11 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='resolved_at',
            field=models.DateTimeField(),
        ),
    ]
