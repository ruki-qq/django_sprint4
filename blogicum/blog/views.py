from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)
from django.views.generic.list import MultipleObjectMixin

from .forms import CommentForm, PostForm
from .models import Category, Comment, Post

User = get_user_model()


def select_posts(only_published=True, **filters):
    published_filters = {'pub_date__lte': timezone.now(), 'is_published': True}
    if not only_published:
        published_filters = {}
    return (
        Post.objects.select_related('category', 'author')
        .prefetch_related('location')
        .filter(**published_filters, **filters)
    )


class PostListMixin:
    model = Post
    paginate_by = 10


class PostActionsMixin:
    model = Post
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse_lazy('blog:index')


class PostListView(PostListMixin, ListView):
    template_name = 'blog/index.html'

    filters = {
        'category__is_published': True,
    }
    queryset = select_posts(**filters)


class CategoryPostListView(PostListMixin, ListView):
    template_name = 'blog/category.html'

    def get_queryset(self):
        filters = {
            'category__slug': self.kwargs['category_slug'],
        }
        return select_posts(**filters)

    def get_context_data(self, **kwargs):
        category = get_object_or_404(
            Category.objects.filter(is_published=True),
            slug=self.kwargs['category_slug'],
        )
        return super().get_context_data(category=category, **kwargs)


class ProfileDetailView(DetailView, MultipleObjectMixin):
    model = User
    template_name = 'blog/profile.html'
    slug_field = 'username'
    context_object_name = 'profile'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        filters = {
            'category__is_published': True,
            'author': self.get_object(),
        }
        return super().get_context_data(
            object_list=select_posts(False, **filters), **kwargs
        )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(form=CommentForm(), **kwargs)


class PostCreateView(PostActionsMixin, LoginRequiredMixin, CreateView):
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(PostActionsMixin, LoginRequiredMixin, UpdateView):
    form_class = PostForm

    def get_success_url(self):
        post_id = self.kwargs['pk']
        return reverse_lazy('blog:post_detail', kwargs={'pk': post_id})

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if not post.author == request.user:
            post_id = self.kwargs['pk']
            return reverse_lazy('blog:post_detail', kwargs={'pk': post_id})
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(PostActionsMixin, LoginRequiredMixin, DeleteView):
    def get_context_data(self, **kwargs):
        return super().get_context_data(
            form=PostForm(instance=self.get_object()), **kwargs
        )

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Post, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


class CommentCreateView(CreateView):
    post = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.birthday = self.post
        return super().form_valid(form)

    def get_success_url(self):
        return 'harosh'
