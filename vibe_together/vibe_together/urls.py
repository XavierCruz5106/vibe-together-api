from django.contrib import admin
from django.urls import path, include
from transactions.urls import router as transactions_router
from rest_framework.schemas import get_schema_view
from rest_framework.renderers import CoreJSONRenderer
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(transactions_router.urls)),  # Include API routes

    path('schema/', SpectacularAPIView.as_view(), name='schema'),  # OpenAPI schema
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Swagger UI
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # ReDoc UI
]
