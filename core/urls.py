"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerUIView
from users.views import (
    CustomTokenObtainPairView, ChangePasswordView,
    RequestPasswordResetView, AdminPasswordResetRequestListView, AdminApprovePasswordResetView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Documentação
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerUIView.as_view(url_name='schema'), name='swagger-ui'),

    # Autenticação JWT
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Usuários
    path('api/users/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('api/users/reset-request/', RequestPasswordResetView.as_view(), name='request_reset'),

    # Admin — solicitações de reset
    path('api/admin/reset-requests/', AdminPasswordResetRequestListView.as_view(), name='admin_list_requests'),
    path('api/admin/reset-requests/<int:pk>/action/', AdminApprovePasswordResetView.as_view(), name='admin_approve_request'),

    # Dispositivos
    path('api/', include('devices.urls')),
]
