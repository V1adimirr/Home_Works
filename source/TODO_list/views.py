from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View, TemplateView

from TODO_list.models import TaskModel


class IndexView(View):
    def get(self, request, *args, **kwargs):
        task = TaskModel.objects.order_by("-updated_at")
        context = {"tasks": task}
        return render(request, "index.html", context)


class TaskView(TemplateView):
    template_name = "task_view.html"

    def get_context_data(self, **kwargs):
        pk = kwargs.get("pk")
        task = get_object_or_404(TaskModel, pk=pk)
        kwargs["task"] = task
        return super().get_context_data(**kwargs)
