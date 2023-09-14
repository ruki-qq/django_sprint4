from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import MyUserCreationForm

User = get_user_model()


class UsersCreateView(CreateView):
    model = User
    template_name = 'registration/registration_form.html'
    form_class = MyUserCreationForm
    success_url = reverse_lazy('blog:index')
