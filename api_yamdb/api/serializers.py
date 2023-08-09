from rest_framework import serializers

from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.StringRelatedField(read_only=True)
    # возможно придется заменить на SlugRelatedField,
    # также и в CommentSerializer

    # score = serializers.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    # не уверена что необходимо

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """Запрещает повторно оставлять отзывы."""

        if self.context.get('request').method != 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('title_id')
        if Review.objects.filter(author_id=author, title_id=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id', 'text', 'author', 'pub_date')
