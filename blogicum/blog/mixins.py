from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse

from .models import Comment, Post


class PostListMixin:
    model = Post
    paginate_by = 10


class PostActionsMixin(LoginRequiredMixin):
    model = Post
    template_name = 'blog/create.html'
    post_pk = 'pk'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return redirect('blog:post_detail', pk=kwargs[self.post_pk])
        return super().dispatch(request, *args, **kwargs)


class CommentActionsMixin:
    model = Comment
    template_name = 'blog/comment.html'
    post_pk = 'post_pk'

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if request.user != comment.author:
            return redirect('blog:post_detail', pk=kwargs[self.post_pk])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'pk': self.kwargs[self.post_pk]}
        )
