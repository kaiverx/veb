from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Developer, Game, UserProfile, Purchase, Review

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ['id', 'developer_name', 'country', 'foundation_date', 'picture']

class GameSerializer(serializers.ModelSerializer):
    developer = DeveloperSerializer(read_only=True)
    developer_id = serializers.PrimaryKeyRelatedField(
        queryset=Developer.objects.all(), write_only=True, source='developer'
    )

    class Meta:
        model = Game
        fields = ['id', 'game_name', 'price', 'score', 'info', 'status',
                  'system_requirements', 'developer', 'developer_id', 'picture']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='user'
    )

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'user_id', 'balance', 'avatar']

class PurchaseSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # когда в api создается сериалайзер,
        # то заполняется специальное поле сериалайзера которое называется context
        # в него добавляется информация по запросе, и доступна эта инфа
        # через self.context['request'], в частности там есть информация о пользователе
        if 'request' in self.context:
            # заполняем validated_data который используется для создания сущности в БД
            # данными из запроса
            validated_data['user'] = self.context['request'].user

        return super().create(validated_data)

    class Meta:
        model = Purchase
        fields = ['id', 'user', 'game', 'purchase_date', 'price_at_purchase']
        read_only_fields = ['user']

class ReviewSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user

        return super().create(validated_data)

    class Meta:
        model = Review
        fields = ['id', 'user', 'game', 'review_text', 'rating', 'created_at']
        read_only_fields = ['user']
