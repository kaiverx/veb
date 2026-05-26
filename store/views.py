from rest_framework import viewsets
from .models import Developer, Game, UserProfile, Purchase, Review
from .serializers import DeveloperSerializer, GameSerializer, UserProfileSerializer, PurchaseSerializer, ReviewSerializer

class DeveloperViewSet(viewsets.ModelViewSet):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        # фильтруем по текущему юзеру
        if self.request.user.is_superuser:
            # суперюзер может фильтровать по юзеру через query param
            user_id = self.request.query_params.get('user_id')
            if user_id:
                qs = qs.filter(user=user_id)
        else:
            qs = qs.filter(user=self.request.user)

        return qs

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        # фильтруем по текущему юзеру
        if self.request.user.is_superuser:
            # суперюзер может фильтровать по юзеру через query param
            user_id = self.request.query_params.get('user_id')
            if user_id:
                qs = qs.filter(user=user_id)
        else:
            qs = qs.filter(user=self.request.user)

        return qs
