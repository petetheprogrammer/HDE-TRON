
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")), #accounts/login
    path("", include("homepage.urls")),
    path("homepage/", include("homepage.urls")),
    path('admin/', admin.site.urls),

]
