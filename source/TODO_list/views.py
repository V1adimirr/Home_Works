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
            types = form.cleaned_data.get('type')
            new_task = TaskModel.objects.create(short_de=short_de, description=description, status=status,
                                                type=types)
            return redirect("view", pk=new_task.pk)
        return render(request, 'task_create.html', {'form': form})

