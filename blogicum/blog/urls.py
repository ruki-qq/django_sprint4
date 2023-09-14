from django.urls import path

from . import views
from .views import (
    ProfileDetailView,
    PostListView,
    PostDetailView,
    CategoryPostListView,
    CommentCreateView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    ProfileUpdateView,
    CommentUpdateView,
    CommentDeleteView,
)

app_name = 'blog'


urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path(
        'posts/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'
    ),
    path(
        'posts/<int:pk>/comment/',
        CommentCreateView.as_view(),
        name='add_comment',
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_pk>/',
        CommentUpdateView.as_view(),
        name='edit_comment',
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_pk>/',
        CommentDeleteView.as_view(),
        name='delete_comment',
    ),
    path(
        'category/<slug:category_slug>/',
        CategoryPostListView.as_view(),
        name='category_posts',
    ),
    path('posts/create/', PostCreateView.as_view(), name='create_post'),
    path('profile/<slug:slug>/', ProfileDetailView.as_view(), name='profile'),
    path(
        'edit_profile/',
        ProfileUpdateView.as_view(),
        name='edit_profile',
    ),
]
