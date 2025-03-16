from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb import constants
from reviews.validators import validate_title_year
from users.models import User


class SlugNameClass(models.Model):
    """Класс слаг."""

    name = models.CharField(
        max_length=constants.MAX_CATEGORYNAME_LENGHT,
        verbose_name='Название',
        help_text='Необходимое названия',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Индификатор',
        help_text='Необходимый индификатор',
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(SlugNameClass):
    """Класс категорий."""

    class Meta(SlugNameClass.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(SlugNameClass):
    """Класс жанров."""

    class Meta(SlugNameClass.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Класс заголовков."""

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
        validators=(validate_title_year,),
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
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
    """Вспомогательный класс, связывающий жанры и произведения."""

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
    """Базовый класс для отзывов и комментариев."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
        help_text='Пользователь, который оставил отзыв',
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Текст, который пишет пользователь',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Дата публикации проставляется автоматически',
    )

    class Meta:
        abstract = True
        ordering = ('pub_date',)

    def __str__(self) -> str:
        return self.text[:constants.MAX_STR_LENGHT]


class Review(BaseClassRewCom):
    """Класс отзывов."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        help_text='Выберите произведение, к которому хотите оставить отзыв',
    )
    score = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(constants.MIN_SCORE_VALUE),
            MaxValueValidator(constants.MAX_SCORE_VALUE),
        ),
        error_messages={
            'validators': (
                f'Оценка должна быть от {constants.MIN_SCORE_VALUE}'
                f'до {constants.MAX_SCORE_VALUE}!'
            ),
        },
        verbose_name='Оценка произведения',
        help_text='Укажите оценку произведения',
    )

    class Meta(BaseClassRewCom.Meta):
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique reviews',
            ),
        )


class Comment(BaseClassRewCom):
    """Класс комментариев."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        help_text='Отзыв, к которому оставляют комментарий',
    )

    class Meta(BaseClassRewCom.Meta):
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
