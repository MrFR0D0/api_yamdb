from django.conf import settings
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status

from api_yamdb import constants
from reviews.models import Category, Comment, Genre, Review, Title
from reviews.validators import validate_title_year
from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=constants.MAX_EMAIL_LENGHT, required=True)
    username = serializers.RegexField(
        regex=constants.USERNAME_CHECK,
        max_length=constants.MAX_USERNAME_LENGHT
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, username):
        if username == settings.NOT_ALLOWED_USERNAME:
            raise serializers.ValidationError(
                "Имя 'me' для username запрещено."
            )
        return username

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        is_user_exists = User.objects.filter(username=username).exists()
        is_email_exists = User.objects.filter(email=email).exists()
        if is_user_exists:
            user = User.objects.get(username=username)
            if user.email != email:
                raise serializers.ValidationError(
                    {"detail": "Неверно указан email пользователя"},
                    status.HTTP_400_BAD_REQUEST,
                )
        if is_email_exists:
            user = User.objects.get(email=email)
            if user.username != username:
                raise serializers.ValidationError(
                    {"detail": "Пользователь с таким email уже существует"},
                    status.HTTP_400_BAD_REQUEST,
                )
        return data


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=constants.USERNAME_CHECK,
        max_length=constants.MAX_USERNAME_LENGHT,
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True,
        max_length=constants.MAX_CONFCODE_LENGHT,
    )

    # def validate_confirmation_code(self, username):
    #     user = get_object_or_404(User, username=request.data['username'])
    #     confirmation_code = self.data.get('confirmation_code')
    #     if not confirmation_code == str(self.user.confirmation_code):
    #         raise serializers.ValidationError(
    #             "Ошибка кода подтверждения."
    #         )
    #     return True


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True,
        allow_empty=False
    )
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        allow_empty=False
    )
    year = serializers.IntegerField()
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        return validate_title_year(value)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        rating = instance.reviews.aggregate(Avg('score'))['score__avg']
        data['rating'] = rating if rating is not None else 0
        return data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    score = serializers.IntegerField()

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, value):
        if not (
            constants.MIN_SCORE_VALUE <= value <= constants.MAX_SCORE_VALUE
        ):
            raise serializers.ValidationError(
                f'Оценка должна быть от {constants.MIN_SCORE_VALUE} '
                f'до {constants.MAX_SCORE_VALUE}!'
            )
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise serializers.ValidationError(
                'Может существовать только один отзыв!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
