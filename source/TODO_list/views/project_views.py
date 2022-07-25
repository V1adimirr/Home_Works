from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView

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
        return render(request, "Projects/project_view.html", kwargs)

