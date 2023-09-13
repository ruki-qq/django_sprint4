from django.urls import path

from . import views
from .views import (
    ProfileDetailView,
    PostListView,
    PostDetailView,
    CategoryPostListView,
    CommentCreateView,
    PostCreateView,
)

app_name = 'blog'


urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path(
        'posts/<int:pk>/comment/',
        CommentCreateView.as_view(),
        name='add_comment',
    ),
    path(
        'category/<slug:category_slug>/',
        CategoryPostListView.as_view(),
        name='category_posts',
    ),
    path('posts/create/', PostCreateView.as_view(), name='create_post'),
    path('profile/<slug:slug>/', ProfileDetailView.as_view(), name='profile'),
]
