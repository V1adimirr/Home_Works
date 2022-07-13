from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic.base import View
from django.views.generic import FormView

from TODO_list.forms import TaskForm
from TODO_list.models import TaskModel
from TODO_list.base_view import FormView as CustomFormView


class IndexView(View):

    def get(self, request):
        task = TaskModel.objects.order_by("-updated_at")
        context = {"tasks": task}
        return render(request, "index.html", context)


class TaskView(View):

    def get(self, request, **kwargs):
        pk = kwargs.get("pk")
        task = get_object_or_404(TaskModel, pk=pk)
        kwargs["task"] = task
        return render(request, "task_view.html", kwargs)


class CreateTask(CustomFormView):
    form_class = TaskForm
    template_name = "task_create.html"

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
        return render(request, "task_delete.html", {"task": task})

    def post(self, request, **kwargs):
        pk = kwargs.get('pk')
        task = get_object_or_404(TaskModel, pk=pk)
        task.delete()
        return redirect("index")


class UpdateTask(FormView):
    form_class = TaskForm
    template_name = "task_update.html"

    def dispatch(self, request, *args, **kwargs):
        self.task = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(TaskModel, pk=self.kwargs.get("pk"))

    def get_success_url(self):
        return reverse("task_view.html", kwargs={"pk": self.task.pk})

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
