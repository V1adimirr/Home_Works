from django.shortcuts import render
from django.views import View

from TODO_list.models import TaskModel

class IndexView(View):
    def get(self, request, *args, **kwargs):
        task = TaskModel.objects.order_by("-updated_at")
        context = {"tasks": task}
        return render(request, "index.html", context)





