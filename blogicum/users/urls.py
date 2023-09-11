from django.urls import include, path

from .views import UsersCreateView


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path(
        'registration/',
        UsersCreateView.as_view(),
        name='registration',
    ),
]
