from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import UpdateView

from TODO_list.forms import UserForm

from TODO_list.models import Project


class CreateUser(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = 'Users/create_user.html'
    form_class = UserForm
    context_key = 'users'
    permission_required = 'TODO_list.add_user'

    def get_success_url(self):
        return reverse('TODO_list:detail_project_view', kwargs={'pk': self.object.pk})

