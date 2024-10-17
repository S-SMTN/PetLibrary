import debug_toolbar
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("Users.urls", namespace="User")),
    path("__debug__/", include(debug_toolbar.urls))
]
