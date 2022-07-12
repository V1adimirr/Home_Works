from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View

from TODO_list.forms import TaskForm
from TODO_list.models import TaskModel


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


class CreateTask(View):

    def get(self, request):
        form = TaskForm()
        return render(request, "task_create.html", {'form': form})

    def post(self, request):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            short_de = form.cleaned_data.get('short_de')
            description = form.cleaned_data.get('description')
            status = form.cleaned_data.get('status')
            type = form.cleaned_data.pop("types")
            new_task = TaskModel.objects.create(short_de=short_de, description=description, status=status)
            new_task.type.set(type)
            return redirect("view", pk=new_task.pk)
        return render(request, 'task_create.html', {'form': form})


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


class UpdateTask(View):

    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        task = get_object_or_404(TaskModel, pk=pk)
        form = TaskForm(initial={
            "short_de": task.short_de,
            "description": task.description,
            "status": task.status,
            "type": task.types.all(),
        })
        return render(request, "task_update.html", {"form": form})

    def post(self, request, **kwargs):
        pk = kwargs.get('pk')
        task = get_object_or_404(TaskModel, pk=pk)
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task.short_de = form.cleaned_data.get("short_de")
            task.description = form.cleaned_data.get("description")
            task.status = form.cleaned_data.get("status")
            task.types.set(form.cleaned_data.pop("types"))
            task.save()
            return redirect("view", pk=task.pk)
        return render(request, "task_update.html", {"form": form})
