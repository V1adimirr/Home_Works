from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from TODO_list.forms import ProjectForm
from TODO_list.models import Project


class IndexProjectView(ListView):
    template_name = 'Projects/list_project_view.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.all()


class DetailProjectView(DetailView):
    template_name = 'Projects/detail_project_view.html'
    model = Project


class CreateProjectView(CreateView):
    template_name = 'Projects/create_project.html'
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('TODO_list:detail_project_view', kwargs={'pk': self.object.pk})

class UpdateProjectView(UpdateView):
    model = Project
    template_name = 'Projects/update_project.html'
    form_class = ProjectForm
    context_key = 'project'

    def get_success_url(self):
        return reverse('TODO_list:detail_project_view', kwargs={'pk': self.object.pk})


class DeleteProjectView(DeleteView):
    template_name = 'Projects/delete_project.html'
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('TODO_list:list_project_view')