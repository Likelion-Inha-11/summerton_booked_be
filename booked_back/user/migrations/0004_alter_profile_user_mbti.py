# Generated by Django 4.2.3 on 2023-07-09 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_profile_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_mbti',
            field=models.CharField(max_length=100),
        ),
    ]