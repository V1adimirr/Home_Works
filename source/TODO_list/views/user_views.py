from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, DeleteView

from TODO_list.forms import UserForm

from TODO_list.models import Project


class CreateUser(UpdateView):
    model = Project
    template_name = 'Users/create_user.html'
    form_class = UserForm
    context_key = 'users'

    def get_success_url(self):
        return reverse('TODO_list:detail_project_view', kwargs={'pk': self.object.pk})

class DeleteUser(DeleteView):
    template_name = 'Users/delete_user.html'
    model = Project
    context_object_name = 'user'

    def get_success_url(self):
        return reverse('TODO_list:detail_project_view', kwargs={'pk': self.object.project.pk})