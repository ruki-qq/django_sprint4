from django.urls import path, include

from . import views
from users.views import ProfileDetailView, ProfileUpdateView

app_name = 'blog'

posts_urls = [
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('create/', views.PostCreateView.as_view(), name='create_post'),
    path(
        '<int:pk>/edit/',
        views.PostUpdateView.as_view(),
        name='edit_post',
    ),
    path(
        '<int:pk>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post',
    ),
    path(
        '<int:pk>/comment/',
        views.CommentCreateView.as_view(),
        name='add_comment',
    ),
    path(
        '<int:post_pk>/edit_comment/<int:pk>/',
        views.CommentUpdateView.as_view(),
        name='edit_comment',
    ),
    path(
        '<int:post_pk>/delete_comment/<int:pk>/',
        views.CommentDeleteView.as_view(),
        name='delete_comment',
    ),
]

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('posts/', include(posts_urls)),
    path(
        'category/<slug:slug>/',
        views.CategoryPostListView.as_view(),
        name='category_posts',
    ),
    path(
        'profile/<slug:slug>/',
        ProfileDetailView.as_view(),
        name='profile',
    ),
    path(
        'edit_profile/',
        ProfileUpdateView.as_view(),
        name='edit_profile',
    ),
]
