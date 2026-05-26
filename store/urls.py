from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'games', views.GameViewSet)
router.register(r'developers', views.DeveloperViewSet)
router.register(r'profiles', views.UserProfilesViewSet)
router.register(r'purchases', views.PurchaseViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'user', views.UserProfileViewSet, basename='user')

urlpatterns = router.urls
