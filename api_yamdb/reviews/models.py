from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import validate_title_year
from users.models import User
from api.constants import MAX_LENGTH_TITLE, MAX_STR_LENGTH

class NamedModel(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_TITLE,
        verbose_name='Название',
        help_text='Необходимое название'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Необходимый идентификатор'
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(NamedModel):
    class Meta(NamedModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(NamedModel):
    class Meta(NamedModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_TITLE,
        verbose_name='Название',
        help_text='Необходимое название произведения',
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
        help_text='Необходимое описание',
    )

    year = models.PositiveSmallIntegerField(
        verbose_name='Дата выхода',
        help_text='Укажите дату выхода',
        validators=(validate_title_year,)
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория',
        help_text='Укажите категорию',
    )

    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр',
        help_text='Укажите жанр',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        help_text='Необходимо произведение',
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр',
        help_text='Необходимый жанр',
    )

    def __str__(self):
        return f'{self.title} {self.genre}'


class AbstractCommentModel(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        help_text='Пользователь, который оставил отзыв или комментарий'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Дата публикации отзыва или комментария, проставляется автоматически.',
    )

    class Meta:
        abstract = True
        ordering = ('pub_date',)

    def __str__(self) -> str:
        return self.text[:MAX_STR_LENGTH]


class Review(AbstractCommentModel):
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        help_text='Выберите произведение, к которому хотите оставить отзыв',
    )
    score = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(settings.MIN_SCORE_VALUE),
            MaxValueValidator(settings.MAX_SCORE_VALUE)
        ),
        error_messages={
            'validators': (
                f'Оценка должна быть от {settings.MIN_SCORE_VALUE}'
                f'до {settings.MAX_SCORE_VALUE}!'
            )
        },
        verbose_name='Оценка произведения',
        help_text='Укажите оценку произведения'
    )

    class Meta(AbstractCommentModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique reviews',
            ),
        )


class Comments(AbstractCommentModel):
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Отзыв, к которому оставляют комментарий'
    )

    class Meta(AbstractCommentModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
