# Generated by Django 4.2.3 on 2023-07-12 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_profile_user_mbti'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to=''),
        ),
    ]
