from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import MyUserCreationForm


class UsersCreateView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = MyUserCreationForm
    success_url = reverse_lazy('pages:homepage')
