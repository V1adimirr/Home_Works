from django.db.models.query_utils import Q
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from TODO_list.forms import TaskForm, SearchForm
from TODO_list.models import TaskModel


class IndexView(ListView):
    model = TaskModel
    template_name = "Tasks/index.html"
    context_object_name = "tasks"
    ordering = ("-updated_at",)
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        if self.search_value:
            query = urlencode({"search": self.search_value})
            context["query"] = query
        return context

    def get_queryset(self):
        if self.search_value:
            return TaskModel.objects.filter(Q(short_de__icontains=self.search_value) |
                                            Q(description__icontains=self.get_search_value()))
        return TaskModel.objects.all()

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class TaskView(DetailView):
    template_name = 'Tasks/task_view.html'
    model = TaskModel


class CreateTask(CreateView):
    form_class = TaskForm
    template_name = "Tasks/task_create.html"

    def form_valid(self, form):
        type = form.cleaned_data.pop("types")
        self.new_task = TaskModel.objects.create(**form.cleaned_data)
        self.new_task.types.set(type)
        return super().form_valid(form)

    def get_redirect_url(self):
        return redirect("TODO_list:view", pk=self.new_task.pk)


class DeleteTask(DeleteView):
    template_name = 'Tasks/task_delete.html'
    model = TaskModel
    context_object_name = 'task'
    success_url = reverse_lazy('TODO_list:list_project_view')


class UpdateTask(UpdateView):
    model = TaskModel
    template_name = 'Tasks/task_update.html'
    form_class = TaskForm
    context_key = 'task'

    def get_success_url(self):
        return reverse('TODO_list:detail_project_view', kwargs={'pk': self.object.pk})