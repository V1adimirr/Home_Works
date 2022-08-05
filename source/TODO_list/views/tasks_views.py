from django.db.models.query_utils import Q
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils.http import urlencode
from django.views.generic.base import View
from django.views.generic import FormView, ListView, CreateView

from TODO_list.forms import TaskForm, SearchForm
from TODO_list.models import TaskModel
from TODO_list.base_view import FormView as CustomFormView


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


class TaskView(View):

    def get(self, request, **kwargs):
        pk = kwargs.get("pk")
        task = get_object_or_404(TaskModel, pk=pk)
        kwargs["task"] = task
        return render(request, "Tasks/task_view.html", kwargs)


class CreateTask(CustomFormView):
    form_class = TaskForm
    template_name = "Tasks/task_create.html"

    def form_valid(self, form):
        type = form.cleaned_data.pop("types")
        self.new_task = TaskModel.objects.create(**form.cleaned_data)
        self.new_task.types.set(type)
        return super().form_valid(form)

    def get_redirect_url(self):
        return redirect("view", pk=self.new_task.pk)


class DeleteTask(View):

    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        task = get_object_or_404(TaskModel, pk=pk)
        return render(request, "Tasks/task_delete.html", {"task": task})

    def post(self, request, **kwargs):
        pk = kwargs.get('pk')
        task = get_object_or_404(TaskModel, pk=pk)
        task.delete()
        return redirect("list_project_view")


class UpdateTask(FormView):
    form_class = TaskForm
    template_name = "Tasks/task_update.html"

    def dispatch(self, request, *args, **kwargs):
        self.task = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(TaskModel, pk=self.kwargs.get("pk"))

    def get_success_url(self):
        return reverse("view", kwargs={"pk": self.task.pk})

    def get_initial(self):
        initial = {}
        for key in "short_de", "description", "status", "types":
            initial[key] = getattr(self.task, key)
        initial['types'] = self.task.types.all()
        return initial

    def form_valid(self, form):
        type = form.cleaned_data.pop("types")
        # self.task.objects.update(**form.cleaned_data) # так тоже работает.
        for key, value in form.cleaned_data.items():
            setattr(self.task, key, value)
        self.task.save()
        self.task.types.set(type)
        return super().form_valid(form)
