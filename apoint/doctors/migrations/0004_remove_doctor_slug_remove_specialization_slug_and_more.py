# Generated by Django 4.1.6 on 2023-10-04 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0003_doctor_slug_specialization_slug_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='specialization',
            name='slug',
        ),
        migrations.AlterField(
            model_name='doctor',
            name='specialization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctors.specialization'),
        ),
    ]
