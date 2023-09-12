from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import MyUserCreationForm

UserModel = get_user_model()


class UserMixin:
    model = UserModel


class UsersCreateView(UserMixin, CreateView):
    template_name = 'registration/registration_form.html'
    form_class = MyUserCreationForm
    success_url = reverse_lazy('pages:homepage')
