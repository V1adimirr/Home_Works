from django.shortcuts import redirect, render
from django.views import View


class FormView(View):
    form_class = None
    template_name = None
    redirect_url = ""

    def get_redirect_url(self):
        return redirect(self.redirect_url)

    def get(self, request):
        form = self.form_class()
        context = self.get_context(form=form)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_isvalid(form)

    def get_context(self, **kwargs):
        return kwargs

    def form_valid(self, form):
        return self.get_redirect_url()

    def form_isvalid(self, form):
        context = self.get_context(form=form)
        return render(self.request, self.template_name, context)


# class CreateTask(View):
#
#     def get(self, request):
#         form = TaskForm()
#         return render(request, "task_create.html", {'form': form})
#
#     def post(self, request):
#         form = TaskForm(data=request.POST)
#         if form.is_valid():
#             short_de = form.cleaned_data.get('short_de')
#             description = form.cleaned_data.get('description')
#             status = form.cleaned_data.get('status')
#             type = form.cleaned_data.pop("types")
#             new_task = TaskModel.objects.create(short_de=short_de, description=description, status=status)
#             new_task.type.set(type)
#             return redirect("view", pk=new_task.pk)
#         return render(request, 'task_create.html', {'form': form})
