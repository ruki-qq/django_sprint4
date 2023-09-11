from django.contrib import admin
from django.urls import include, path

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.internal_server_error'

urlpatterns = [
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
]
