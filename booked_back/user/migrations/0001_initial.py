# Generated by Django 4.2.3 on 2023-07-05 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('userID', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('nickname', models.CharField(max_length=15)),
                ('user_mbti', models.CharField(max_length=4)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
