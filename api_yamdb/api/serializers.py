import datetime

from rest_framework import serializers

from reviews.models import Categories, Genre, User, Review, Title, Comments


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'reviews', 'pub_date')
        read_only_fields = ('reviews', 'author')


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Categories.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'genre', 'category', 'description'
        )

    def validate_year(self, value):
        """Валидация года выпуска произведения."""
        current_year = datetime.date.today().year
        if not 0 <= value <= current_year:
            raise serializers.ValidationError(
                "Проверьте год создания произведения"
                "(не может быть больше текущего)."
            )
        return value


class TitlesReadSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'genre', 'category', 'description', 'rating'
        )


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        exclude = ('title',)

    def validate(self, attrs):
        is_exist = Review.objects.filter(
            author=self.context['request'].user,
            title=self.context['view'].kwargs.get('title_id')).exists()
        if is_exist and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Ваш отзыв на это название уже существует')
        return attrs

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Оценкой может быть целое число в диапазоне от 1 до 10.'
            )
        return value


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class AdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено.'
            )
        return value


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено.'
            )
        return value

    def create(self, validated_data):
        user = User.objects.create(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
