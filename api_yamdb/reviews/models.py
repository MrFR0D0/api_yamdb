from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import validate_title_year
from users.models import User

from api_yamdb import constants


class BaseClass(models.Model):
    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(BaseClass):
    name = models.CharField(
        max_length=constants.MAX_CATEGORYNAME_LENGHT,
        verbose_name='Название',
        help_text='Необходимое названия котегории'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Индификатор',
        help_text='Необходимый индификатор категории',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseClass):
    name = models.CharField(
        max_length=constants.MAX_GENRENAME_LENGHT,
        verbose_name='Название',
        help_text='Необходимое названия жанра',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Необходимый индификатор жанра',
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        max_length=constants.MAX_TITLENAME_LENGHT,
        verbose_name='Название',
        help_text='Необходимое название произведения',
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
        help_text='Необходимое описание',
    )

    year = models.SmallIntegerField(
        verbose_name='Дата выхода',
        help_text='Укажите дату выхода',
        validators=(validate_title_year,)
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        # related_name='titles',
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
        default_related_name = 'titles'
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

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


class BaseClassRewCom(models.Model):
    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self) -> str:
        return self.text[:constants.MAX_STR_LENGHT]


class Review(BaseClassRewCom):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
        help_text='Пользователь, который оставил отзыв',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        help_text='Выберите произведение, к которому хотите оставить отзыв',
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    score = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(constants.MIN_SCORE_VALUE),
            MaxValueValidator(constants.MAX_SCORE_VALUE)
        ),
        error_messages={
            'validators': (
                f'Оценка должна быть от {constants.MIN_SCORE_VALUE}'
                f'до {constants.MAX_SCORE_VALUE}!'
            )
        },
        verbose_name='Оценка произведения',
        help_text='Укажите оценку произведения'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Дата публикации отзыва, проставляется автоматически.',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique reviews',
            ),
        )


class Comments(BaseClassRewCom):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
        help_text='Пользователь, который оставил комментарий'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Отзыв, к которому оставляют комментарий'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Текст комментария, который пишет пользователь'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации комментария',
        help_text='Дата публикации проставляется автоматически'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
