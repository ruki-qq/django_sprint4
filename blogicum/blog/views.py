from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CommentForm, PostForm
from .mixins import CommentActionsMixin, PostActionsMixin, PostListMixin
from .models import Category, Post
from core.utils import select_posts

UserModel = get_user_model()


class PostListView(PostListMixin, ListView):
    template_name = 'blog/index.html'

    def get_queryset(self):
        filters = {
            'category__is_published': True,
        }
        return select_posts(**filters)


class CategoryPostListView(PostListMixin, ListView):
    template_name = 'blog/category.html'
    category_slug = 'slug'

    def get_queryset(self):
        filters = {
            'category__slug': self.kwargs[self.category_slug],
        }
        return select_posts(**filters)

    def get_context_data(self, **kwargs):
        category = get_object_or_404(
            Category.objects.filter(is_published=True),
            slug=self.kwargs[self.category_slug],
        )
        return super().get_context_data(category=category, **kwargs)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    post_pk = 'pk'

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs[self.post_pk])
        if (
            not (
                post.is_published
                and post.category.is_published
                and post.pub_date <= timezone.now()
            )
            and request.user != post.author
        ):
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            form=CommentForm(),
            comments=self.object.comments.select_related('author'),
            **kwargs,
        )


class PostCreateView(PostActionsMixin, CreateView):
    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        return super(PostActionsMixin, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'slug': self.request.user})


class PostUpdateView(PostActionsMixin, UpdateView):
    form_class = PostForm

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'pk': self.kwargs[self.post_pk]}
        )


class PostDeleteView(PostActionsMixin, DeleteView):
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            form=PostForm(instance=self.get_object()), **kwargs
        )


class CommentCreateView(CommentActionsMixin, LoginRequiredMixin, CreateView):
    post_obj = None
    form_class = CommentForm
    post_pk = 'pk'

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(Post, pk=kwargs[self.post_pk])
        return super(CommentActionsMixin, self).dispatch(
            request, *args, **kwargs
        )

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_obj
        return super().form_valid(form)


class CommentUpdateView(CommentActionsMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteView(CommentActionsMixin, DeleteView):
    pass
