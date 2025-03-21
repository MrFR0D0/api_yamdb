from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    """Класс администрирования раздела категорий."""

    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    empty_value_diplay = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    """Класс администрирования раздела жанров."""

    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    empty_value_diplay = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    """Класс администрирования раздела заголовков."""

    list_display = ('pk', 'name', 'description', 'year', 'category')
    search_fields = ('name',)
    list_filter = ('year', 'category')
    empty_value_diplay = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    """Класс администрирования раздела отзывов."""

    list_display = ('pk', 'author', 'text', 'pub_date')
    search_fields = ('author__username', 'text')
    list_filter = ('author', 'pub_date')
    empty_value_diplay = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    """Класс администрирования раздела комментариев."""

    list_display = ('pk', 'author', 'review', 'text', 'pub_date')
    search_fields = ('author__username', 'review')
    list_filter = ('author', 'review', 'pub_date')
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
