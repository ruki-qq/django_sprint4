from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic.list import MultipleObjectMixin

from .forms import MyUserCreationForm
from core.utils import select_posts

UserModel = get_user_model()


class UsersCreateView(CreateView):
    model = UserModel
    template_name = 'registration/registration_form.html'
    form_class = MyUserCreationForm
    success_url = reverse_lazy('blog:index')


class ProfileDetailView(DetailView, MultipleObjectMixin):
    model = UserModel
    template_name = 'blog/profile.html'
    slug_field = 'username'
    context_object_name = 'profile'
    paginate_by = 10
    profile_slug = 'slug'

    def get_context_data(self, **kwargs):
        filters = {
            'author': self.get_object(),
        }
        if self.kwargs[self.profile_slug] != self.request.user.username:
            filters['category__is_published'] = True
            only_published = True
        else:
            only_published = False
        return super().get_context_data(
            object_list=select_posts(only_published, **filters), **kwargs
        )


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserModel
    template_name = 'blog/user.html'
    fields = ('username', 'email', 'first_name', 'last_name')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'slug': self.request.user})
