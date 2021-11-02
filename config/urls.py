from django.urls import path, include
from django.conf.urls import url
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_url_patterns = [
    path("users", include("users.urls")),
    path("postings", include("postings.urls")),
]

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="AIMMO Assignment API",
        default_version="v1",
        description="에이모 기업과제 API Document",
        terms_of_service="https://policies.google.com/terms",
    ),
    validators=["flex"],
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_patterns,
)

urlpatterns = [
    path("users", include("users.urls")),
    path("postings", include("postings.urls")),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
