# Generated by Django 4.1.4 on 2023-05-17 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appointments", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="appoinment",
            name="duration",
            field=models.IntegerField(
                choices=[
                    (15, "15 minutes"),
                    (30, "30 minutes"),
                    (45, "45 minutes"),
                    (60, "1 hour"),
                ],
                default=30,
            ),
        ),
        migrations.AlterField(
            model_name="appoinment",
            name="time",
            field=models.CharField(
                choices=[
                    ("08:00", "08:00"),
                    ("08:15", "08:15"),
                    ("08:30", "08:30"),
                    ("08:45", "08:45"),
                    ("09:00", "09:00"),
                    ("09:15", "09:15"),
                    ("09:30", "09:30"),
                    ("09:45", "09:45"),
                    ("10:00", "10:00"),
                    ("10:15", "10:15"),
                    ("10:30", "10:30"),
                    ("10:45", "10:45"),
                    ("11:00", "11:00"),
                    ("11:15", "11:15"),
                    ("11:30", "11:30"),
                    ("11:45", "11:45"),
                    ("12:00", "12:00"),
                    ("12:15", "12:15"),
                    ("12:30", "12:30"),
                    ("12:45", "12:45"),
                    ("13:00", "13:00"),
                    ("13:15", "13:15"),
                    ("13:30", "13:30"),
                    ("13:45", "13:45"),
                    ("14:00", "14:00"),
                ],
                default=None,
                max_length=15,
            ),
        ),
    ]
