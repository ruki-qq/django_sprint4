from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404
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
        .annotate(comment_count=Count('comments'))
        .order_by('-pub_date')
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
        only_published = (
            False
            if self.kwargs['slug'] == self.request.user.username
            else True
        )
        return super().get_context_data(
            object_list=select_posts(only_published, **filters), **kwargs
        )


class ProfileUpdateView(UpdateView):
    model = User
    template_name = 'blog/user.html'
    fields = ('username', 'email', 'first_name', 'last_name')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'slug': self.request.user})


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if request.user != post.author:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            form=CommentForm(),
            comments=self.object.comments.select_related('author'),
            **kwargs,
        )


class PostCreateView(PostActionsMixin, LoginRequiredMixin, CreateView):
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'slug': self.request.user})


class PostUpdateView(PostActionsMixin, LoginRequiredMixin, UpdateView):
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'pk': self.kwargs['pk']}
        )

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return redirect('blog:post_detail', pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(PostActionsMixin, LoginRequiredMixin, DeleteView):
    def get_context_data(self, **kwargs):
        return super().get_context_data(
            form=PostForm(instance=self.get_object()), **kwargs
        )

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return redirect('blog:post_detail', pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)


class CommentCreateView(LoginRequiredMixin, CreateView):
    post_obj = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_obj
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['pk']})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm
    pk_url_kwarg = 'comment_pk'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'pk': self.kwargs['post_id']}
        )

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        print(comment)
        if comment.author != request.user:
            return redirect('blog:post_detail', pk=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm
    pk_url_kwarg = 'comment_pk'

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            form=PostForm(instance=self.get_object()), **kwargs
        )

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'pk': self.kwargs['post_id']}
        )
