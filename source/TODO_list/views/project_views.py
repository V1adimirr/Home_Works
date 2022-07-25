from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView

from TODO_list.forms import ProjectForm
from TODO_list.models import Project, TaskModel


class IndexProjectView(ListView):
    template_name = 'Projects/list_project_view.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.all()


class DetailProjectView(DetailView):
    def get(self, request, **kwargs):
        pk = kwargs.get("pk")
        project = get_object_or_404(Project, pk=pk)
        kwargs["project"] = project
        return render(request, "Projects/detail_project_view.html", kwargs)


class CreateProjectView(CreateView):
    template_name = 'Projects/create_project.html'
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('detail_project_view', kwargs={'pk': self.object.pk})
