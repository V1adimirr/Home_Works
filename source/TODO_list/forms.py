from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from TODO_list.models import TaskModel, Project


class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ["short_de", "description", "status", "types"]
        widgets = {
            "types": widgets.CheckboxSelectMultiple,
            "description": widgets.Textarea(attrs={"cols": 20, "rows": 6})
        }

    def clean_short_de(self):
        short_de = self.cleaned_data.get("short_de")
        if len(short_de) > 200:
            raise ValidationError("Краткое описание должно быть короче 200 символов")
        return short_de

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if len(description) < 10:
            raise ValidationError("Описание задачи должно быть длинее 10 символов")
        return description


class SearchForm(forms.Form):
    search = forms.CharField(max_length=20, required=False, label="Поиск")


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name_project', 'project_de', 'created_time', 'updated_time']
        widgets = {
            "project_de": forms.Textarea(attrs={"cols": 20, "rows": 6}),
            "created_time": forms.SelectDateWidget,
            "updated_time": forms.SelectDateWidget,

        }
