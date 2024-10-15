from django.urls import path
from django.contrib import admin

from Library.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index)
]
