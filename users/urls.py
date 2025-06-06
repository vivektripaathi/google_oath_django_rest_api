from django.urls import include, path

from users.presentation import urls as users_urls
app_name = "users"

urlpatterns = [
    path("", include(users_urls)),
]