import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import TEXT_LIMIT


class Users:
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    ROLE_CHOICES = [
        (Users.USER, 'Пользователь'),
        (Users.MODERATOR, 'Модератор'),
        (Users.ADMIN, 'Администратор'),
    ]
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=150, blank=True)
    role = models.CharField(
        max_length=255,
        choices=ROLE_CHOICES,
        default=Users.USER,
        verbose_name='Роль')
    bio = models.TextField(null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username

    @property
    def is_admin(self):
        return self.role == Users.ADMIN

    @property
    def is_moderator(self):
        return self.role == Users.MODERATOR

    @property
    def is_user(self):
        return self.role == Users.USER


class Categories(models.Model):
    """Модель категорий."""
    name = models.CharField(
        'Имя категории',
        max_length=50,
        help_text='Дайте название категории',
    )
    slug = models.SlugField('Адрес группы', unique=True)

    def __str__(self):
        """Возвращаем название категории."""
        return self.name


class Genre(models.Model):
    """Модель жанра."""
    name = models.CharField(
        'Имя жанра',
        max_length=30,
        help_text='Дайте название жанру',
    )
    slug = models.SlugField('Адрес жанра', unique=True)

    def __str__(self):
        """Возвращаем название жанра."""
        return self.name


class Title(models.Model):
    """Модель произведения."""
    name = models.CharField(
        'Название произведения',
        max_length=50,
        null=False,
    )
    year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0), MaxValueValidator(datetime.date.today().year)
        ],
        verbose_name='год выпуска'
    )
    category = models.ForeignKey(
        Categories,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория произведения',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр произведения',
    )
    description = models.TextField()

    def __str__(self):
        """Возвращаем название произведения."""
        return self.name


class Review(models.Model):
    """Модель отзыва."""
    text = models.TextField(null=False)
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='рейтинг'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author')
        ]

    def __str__(self):
        """Возвращаем первые 20 символов отзыва."""
        return self.text[:TEXT_LIMIT]


class Comments(models.Model):
    """Модель комментария."""
    text = models.TextField(null=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    reviews = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        """Подпись автора комментария."""
        return f'comments by {self.author}'
