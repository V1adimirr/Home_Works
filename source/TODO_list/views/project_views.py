from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from TODO_list.forms import ProjectForm, SearchForm
from TODO_list.models import Project


class IndexProjectView(ListView):
    template_name = 'Projects/list_project_view.html'
    context_object_name = 'projects'
    paginate_by = 4

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
            return Project.objects.filter(Q(name_project__icontains=self.search_value))
        return Project.objects.all()

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class DetailProjectView(DetailView):
    template_name = 'Projects/detail_project_view.html'
    model = Project
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = self.object.users.order_by()
        return context


class CreateProjectView(PermissionRequiredMixin, CreateView):
    template_name = 'Projects/create_project.html'
    form_class = ProjectForm
    permission_required = 'TODO_list.add_project'

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('TODO_list:detail_project_view', kwargs={'pk': self.object.pk})


class UpdateProjectView(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = 'Projects/update_project.html'
    form_class = ProjectForm
    context_key = 'project'
    permission_required = 'TODO_list.change_project'

    def get_success_url(self):
        return reverse('TODO_list:detail_project_view', kwargs={'pk': self.object.pk})


class DeleteProjectView(PermissionRequiredMixin, DeleteView):
    template_name = 'Projects/delete_project.html'
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('TODO_list:list_project_view')
    permission_required = 'TODO_list.delete_project'
