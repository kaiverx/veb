from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # для редиректа

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('store.urls')),  # маршруты API
    path('', RedirectView.as_view(url='/api/', permanent=False)),  # редирект с корня
]
