# Generated by Django 5.1.2 on 2024-12-23 16:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0010_alter_feedback_page_name_alter_feedback_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="feedback",
            name="is_send",
            field=models.BooleanField(default=False),
        ),
    ]