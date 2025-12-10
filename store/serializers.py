from rest_framework import serializers
from .models import Developer, Game, UserProfile, Purchase, Review

# Сначала сериализатор для Developer
class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ['id', 'developer_name', 'country', 'foundation_date']

# Потом сериализатор для Game, с вложенным DeveloperSerializer
class GameSerializer(serializers.ModelSerializer):
    developer = DeveloperSerializer(read_only=True)  # показываем только данные разработчика
    developer_id = serializers.PrimaryKeyRelatedField(
        queryset=Developer.objects.all(), write_only=True, source='developer'
    )  # для создания/обновления

    class Meta:
        model = Game
        fields = ['id', 'game_name', 'price', 'score', 'info', 'status', 'system_requirements', 'developer', 'developer_id']

# Сериализатор UserProfile
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'balance', 'avatar']

# Сериализатор Purchase
class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'user', 'game', 'purchase_date', 'price_at_purchase']

# Сериализатор Review
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'game', 'review_text', 'rating', 'created_at']
