from django.shortcuts import reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from TODO_list.forms import TaskForm
from TODO_list.models import TaskModel, Project


class IndexView(ListView):
    model = TaskModel
    template_name = "Tasks/index.html"
    context_object_name = "tasks"
    ordering = ("-updated_at",)
    paginate_by = 4


class TaskView(DetailView):
    template_name = 'Tasks/task_view.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.object.project.order_by()
        return context


class CreateTask(CreateView):
    form_class = TaskForm
    template_name = "Tasks/task_create.html"
    model = Project

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        print(project.pk)
        form.instance.project = project
        print(form.instance)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("TODO_list:view", kwargs={"pk": self.object.project.pk})


class DeleteTask(DeleteView):
    template_name = 'Tasks/task_delete.html'
    model = TaskModel
    context_object_name = 'task'
    success_url = reverse_lazy('TODO_list:list_project_view')


class UpdateTask(UpdateView):
    form_class = TaskForm
    template_name = 'Tasks/task_update.html'
    model = TaskModel
    context_key = 'task'

    def get_success_url(self):
        return reverse('TODO_list:detail_project_view', kwargs={'pk': self.object.project.pk})
