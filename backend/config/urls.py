from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .spa import spa

admin.site.site_header = "Pathwise admin"
admin.site.site_title = "Pathwise"
admin.site.index_title = "Student skill and career roadmap"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api/auth/", include("accounts.urls")),
    path("api/", include("catalog.urls")),
    re_path(r"^(?P<resource>.*)$", spa, name="spa"),
]
