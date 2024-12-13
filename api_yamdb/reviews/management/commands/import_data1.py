import logging
from csv import DictReader

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import CustomUser
from api.constants import CSV_DIR

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Импорт данных из csv файлов'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Принудительно импортировать данные, даже если они уже существуют.',
        )

    def handle(self, *args, **kwargs):
        force = kwargs['force']
        data_imports = [
            (CustomUser, 'users.csv', self.create_user, 'Данные для User'),
            (Genre, 'genre.csv', self.create_genre, 'Данные для Genre'),
            (Category, 'category.csv', self.create_category, 'Данные для Category'),
            (Title, 'titles.csv', self.create_title, 'Данные для Title'),
            (GenreTitle, 'genre_title.csv', self.create_genre_title, 'Данные для GenreTitle'),
            (Review, 'review.csv', self.create_review, 'Данные для Review'),
            (Comment, 'comments.csv', self.create_comment, 'Данные для Comments'),
        ]

        for model, filename, create_method, data_label in data_imports:
            self.import_data(model, filename, create_method, data_label, force)

    def import_data(self, model, filename, create_method, data_label, force):
        """Импорт данных из csv файла."""
        if not force and model.objects.exists():
            logger.info(f'{data_label} уже загружены. Используйте --force для повторного импорта.')
            return

        try:
            with open(CSV_DIR / filename, encoding='utf8') as csvfile:
                for row in DictReader(csvfile):
                    create_method(row)
            logger.info(f'{data_label} загружены.')
        except Exception as e:
            logger.error(f'Ошибка при импорте данных из {filename}: {e}')

    def create_user(self, row):
        CustomUser.objects.create(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            role=row['role'],
            bio=row['bio'],
            first_name=row['first_name'],
            last_name=row['last_name'],
        )

    def create_genre(self, row):
        Genre.objects.create(
            id=row['id'],
            name=row['name'],
            slug=row['slug'],
        )

    def create_category(self, row):
        Category.objects.create(
            id=row['id'],
            name=row['name'],
            slug=row['slug'],
        )

    def create_title(self, row):
        Title.objects.create(
            id=row['id'],
            name=row['name'],
            year=row['year'],
            category=Category.objects.get(id=row['category']),
        )

    def create_genre_title(self, row):
        GenreTitle.objects.create(
            id=row['id'],
            title_id=row['title_id'],
            genre_id=row['genre_id'],
        )

    def create_review(self, row):
        Review.objects.create(
            id=row['id'],
            title_id=row['title_id'],
            text=row['text'],
            author=CustomUser.objects.get(id=row['author']),
            score=row['score'],
            pub_date=row['pub_date'],
        )

    def create_comment(self, row):
        Comment.objects.create(
            id=row['id'],
            review_id=row['review_id'],
            text=row['text'],
            author=CustomUser.objects.get(id=row['author']),
            pub_date=row['pub_date'],
        )
