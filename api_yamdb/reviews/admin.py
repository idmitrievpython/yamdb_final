from django.contrib import admin

from .models import Categories, Comments, Genre, Review, Title, User

admin.site.register(User)


@admin.register(Title)
class TitlesAdmin(admin.ModelAdmin):
    """Настройка отображения произведения в админке."""
    list_display = (
        'pk',
        'name',
        'year',
        'category',
        'description',
    )
    list_filter = ('name',)
    search_fields = ('description',)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    """Отображение категорий в админке."""
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Отображение жанров в админке."""
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    """Отображение отзывов в админке."""
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'score',
    )
    search_fields = ('text',)
    list_filter = ('pub_date',)


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    """Отображение комментариев в админке."""
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
    )
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
