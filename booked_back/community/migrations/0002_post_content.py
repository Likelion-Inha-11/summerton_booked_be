# Generated by Django 4.2.3 on 2023-07-09 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.TextField(null=True),
        ),
    ]