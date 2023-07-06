# Generated by Django 4.2.3 on 2023-07-06 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='EI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Feeling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='FT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='JP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='NS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='NSCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mention_count', models.IntegerField(default=0)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.ns')),
            ],
        ),
        migrations.CreateModel(
            name='JPCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mention_count', models.IntegerField(default=0)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.jp')),
            ],
        ),
        migrations.CreateModel(
            name='GenreCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mention_count', models.IntegerField(default=0)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.genre')),
            ],
        ),
        migrations.CreateModel(
            name='FTCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mention_count', models.IntegerField(default=0)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.ft')),
            ],
        ),
        migrations.CreateModel(
            name='FillingCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mention_count', models.IntegerField(default=0)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.feeling')),
            ],
        ),
        migrations.CreateModel(
            name='EICount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mention_count', models.IntegerField(default=0)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.ei')),
            ],
        ),
        migrations.CreateModel(
            name='BookReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_title', models.CharField(max_length=255)),
                ('book_title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='book.book')),
                ('ei', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='book.ei')),
                ('feeling', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='book.feeling')),
                ('ft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='book.ft')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='book.genre')),
                ('jp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='book.jp')),
                ('ns', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='book.ns')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='ei',
            field=models.ManyToManyField(related_name='books', through='book.EICount', to='book.ei'),
        ),
        migrations.AddField(
            model_name='book',
            name='fellings',
            field=models.ManyToManyField(related_name='books', through='book.FillingCount', to='book.feeling'),
        ),
        migrations.AddField(
            model_name='book',
            name='ft',
            field=models.ManyToManyField(related_name='books', through='book.FTCount', to='book.ft'),
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(related_name='books', through='book.GenreCount', to='book.genre'),
        ),
        migrations.AddField(
            model_name='book',
            name='jp',
            field=models.ManyToManyField(related_name='books', through='book.JPCount', to='book.jp'),
        ),
        migrations.AddField(
            model_name='book',
            name='ns',
            field=models.ManyToManyField(related_name='books', through='book.NSCount', to='book.ns'),
        ),
    ]
