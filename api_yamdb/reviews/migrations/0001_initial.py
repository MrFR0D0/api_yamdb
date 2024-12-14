# Generated by Django 3.2 on 2024-12-14 06:00

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import reviews.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Необходимое названия', max_length=256, verbose_name='Название')),
                ('slug', models.SlugField(help_text='Необходимый индификатор', unique=True, verbose_name='Индификатор')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Текст, который пишет пользователь', verbose_name='Текст')),
                ('pub_date', models.DateTimeField(auto_now_add=True, help_text='Дата публикации проставляется автоматически', verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('pub_date',),
                'abstract': False,
                'default_related_name': 'comments',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Необходимое названия', max_length=256, verbose_name='Название')),
                ('slug', models.SlugField(help_text='Необходимый индификатор', unique=True, verbose_name='Индификатор')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ('name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Текст, который пишет пользователь', verbose_name='Текст')),
                ('pub_date', models.DateTimeField(auto_now_add=True, help_text='Дата публикации проставляется автоматически', verbose_name='Дата публикации')),
                ('score', models.PositiveSmallIntegerField(error_messages={'validators': 'Оценка должна быть от 1до 10!'}, help_text='Укажите оценку произведения', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Оценка произведения')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ('pub_date',),
                'abstract': False,
                'default_related_name': 'reviews',
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Необходимое название произведения', max_length=256, verbose_name='Название')),
                ('description', models.TextField(blank=True, help_text='Необходимое описание', null=True, verbose_name='Описание')),
                ('year', models.SmallIntegerField(help_text='Укажите дату выхода', validators=[reviews.validators.validate_title_year], verbose_name='Дата выхода')),
                ('category', models.ForeignKey(help_text='Укажите категорию', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.category', verbose_name='Категория')),
                ('genre', models.ManyToManyField(help_text='Укажите жанр', related_name='titles', through='reviews.GenreTitle', to='reviews.Genre', verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
                'ordering': ('name',),
                'default_related_name': 'titles',
            },
        ),
    ]
