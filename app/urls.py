from django.urls import path, include
from rest_framework.routers import DefaultRouter
from store import views 

router = DefaultRouter()
router.register(r'games', views.GameViewSet)
router.register(r'developers', views.DeveloperViewSet)
router.register(r'profiles', views.UserProfileViewSet)
router.register(r'purchases', views.PurchaseViewSet)
router.register(r'reviews', views.ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
