import datetime
import pyotp
from io import BytesIO

import pandas as pd

from django.core.cache import cache
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from rest_framework import viewsets, serializers
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
from django.db.models import Avg, Count, Max, Min

from .models import Developer, Game, UserProfile, Purchase, Review
from .serializers import DeveloperSerializer, GameSerializer, UserProfileSerializer, PurchaseSerializer, ReviewSerializer


class OTPRequired(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and cache.get(f'otp_good_{request.user.id}', False))


class UserProfileViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]

    class OTPSerializer(serializers.Serializer):
        key = serializers.CharField()

    class LoginSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()

    @action(detail=False, url_path="check-login", methods=['GET'], permission_classes=[])
    def get_check_login(self, request, *args, **kwargs):
        return Response({
            'is_authenticated': self.request.user.is_authenticated
        })

    @action(detail=False, url_path="login", methods=['POST'], permission_classes=[])
    def use_login(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
        return Response({
            'is_authenticated': bool(user)
        })

    @action(detail=False, url_path="logout", methods=['POST'], permission_classes=[])
    def use_logout(self, request, *args, **kwargs):
        logout(request)
        return Response({'success': True})

    @action(detail=False, url_path='otp-login', methods=['POST'])
    def otp_login(self, request, *args, **kwargs):
        profile = request.user.profile
        if not profile.otp_key:
            profile.otp_key = pyotp.random_base32()
            profile.save()

        totp = pyotp.TOTP(profile.otp_key)

        serializer = self.OTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        success = False
        if totp.verify(serializer.validated_data['key'], valid_window=1):
            cache.set(f'otp_good_{request.user.id}', True, 300)
            success = True

        return Response({'success': success})

    @action(detail=False, url_path='otp-status', methods=['GET'])
    def get_otp_status(self, request, *args, **kwargs):
        otp_good = cache.get(f'otp_good_{request.user.id}', False)
        return Response({'otp_good': otp_good})

    @action(detail=False, url_path='otp-key', methods=['GET'])
    def get_otp_key(self, request, *args, **kwargs):
        profile = request.user.profile
        if not profile.otp_key:
            profile.otp_key = pyotp.random_base32()
            profile.save()
        totp = pyotp.TOTP(profile.otp_key)
        return Response({
            'otp_key': profile.otp_key,
            'otp_uri': totp.provisioning_uri(name=request.user.username, issuer_name='GameStore')
        })

    @action(detail=False, url_path='info', methods=['GET'], permission_classes=[])
    def get_info(self, request, *args, **kwargs):
        is_auth = request.user.is_authenticated
        otp_good = cache.get(f'otp_good_{request.user.id}', False) if is_auth else False
        return Response({
            'is_authenticated': is_auth,
            'is_superuser': request.user.is_superuser if is_auth else False,
            'username': request.user.username if is_auth else None,
            'otp_good': otp_good,
        })


class DeveloperViewSet(viewsets.ModelViewSet):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), OTPRequired()]
        return []

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request):
        stats = Developer.objects.aggregate(count=Count("*"))
        return Response(self.StatsSerializer(instance=stats).data)

    @action(detail=False, methods=["GET"], url_path="export-excel")
    def export_excel(self, request):
        try:
            qs = Developer.objects.all()
            data = []
            for item in qs:
                data.append({
                    "ID": item.id,
                    "Название": item.developer_name,
                    "Страна": item.country,
                    "Дата основания": str(item.foundation_date),
                })
            df = pd.DataFrame(data)
            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Разработчики")
            output.seek(0)
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            filename = f"developers_{today}.xlsx"
            response = HttpResponse(
                output.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), OTPRequired()]
        return []

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.FloatField()
        min = serializers.FloatField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request):
        stats = Game.objects.aggregate(
            count=Count("*"),
            avg=Avg("price"),
            max=Max("price"),
            min=Min("price"),
        )
        return Response(self.StatsSerializer(instance=stats).data)

    @action(detail=False, methods=["GET"], url_path="export-excel")
    def export_excel(self, request):
        try:
            qs = Game.objects.all()
            data = []
            for item in qs:
                data.append({
                    "ID": item.id,
                    "Название": item.game_name,
                    "Цена": str(item.price),
                    "Оценка": item.score,
                    "Статус": item.status,
                    "Разработчик": item.developer.developer_name if item.developer else "",
                })
            df = pd.DataFrame(data)
            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Игры")
            output.seek(0)
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            filename = f"games_{today}.xlsx"
            response = HttpResponse(
                output.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class UserProfilesViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), OTPRequired()]
        return []

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.FloatField()
        min = serializers.FloatField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request):
        stats = UserProfile.objects.aggregate(
            count=Count("*"),
            avg=Avg("balance"),
            max=Max("balance"),
            min=Min("balance"),
        )
        return Response(self.StatsSerializer(instance=stats).data)

    @action(detail=False, methods=["GET"], url_path="export-excel")
    def export_excel(self, request):
        try:
            qs = UserProfile.objects.all()
            data = []
            for item in qs:
                data.append({
                    "ID": item.id,
                    "Пользователь": item.user.username,
                    "Баланс": str(item.balance),
                })
            df = pd.DataFrame(data)
            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Профили")
            output.seek(0)
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            filename = f"profiles_{today}.xlsx"
            response = HttpResponse(
                output.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), OTPRequired()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_authenticated:
            return qs.none()
        if self.request.user.is_superuser:
            user_id = self.request.query_params.get('user_id')
            if user_id:
                qs = qs.filter(user=user_id)
        else:
            qs = qs.filter(user=self.request.user)
        return qs

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.FloatField()
        min = serializers.FloatField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request):
        stats = self.get_queryset().aggregate(
            count=Count("*"),
            avg=Avg("price_at_purchase"),
            max=Max("price_at_purchase"),
            min=Min("price_at_purchase"),
        )
        return Response(self.StatsSerializer(instance=stats).data)

    @action(detail=False, methods=["GET"], url_path="export-excel")
    def export_excel(self, request):
        try:
            qs = self.get_queryset()
            data = []
            for item in qs:
                data.append({
                    "ID": item.id,
                    "Пользователь": item.user.username,
                    "Игра": item.game.game_name,
                    "Цена покупки": str(item.price_at_purchase),
                    "Дата покупки": str(item.purchase_date),
                })
            df = pd.DataFrame(data)
            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Покупки")
            output.seek(0)
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            filename = f"purchases_{today}.xlsx"
            response = HttpResponse(
                output.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), OTPRequired()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_authenticated:
            return qs.none()
        if self.request.user.is_superuser:
            user_id = self.request.query_params.get('user_id')
            if user_id:
                qs = qs.filter(user=user_id)
        else:
            qs = qs.filter(user=self.request.user)
        return qs

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request):
        stats = self.get_queryset().aggregate(
            count=Count("*"),
            avg=Avg("rating"),
            max=Max("rating"),
            min=Min("rating"),
        )
        return Response(self.StatsSerializer(instance=stats).data)

    @action(detail=False, methods=["GET"], url_path="export-excel")
    def export_excel(self, request):
        try:
            qs = self.get_queryset()
            data = []
            for item in qs:
                data.append({
                    "ID": item.id,
                    "Пользователь": item.user.username,
                    "Игра": item.game.game_name,
                    "Текст отзыва": item.review_text,
                    "Оценка": item.rating,
                })
            df = pd.DataFrame(data)
            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Отзывы")
            output.seek(0)
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            filename = f"reviews_{today}.xlsx"
            response = HttpResponse(
                output.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=500)
