from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from TODO_list.models import  TaskModel


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
        if len(short_de) > 20:
            raise ValidationError("Краткое описание должно быть короче 20 символов")
        return short_de

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if len(description) < 100:
            raise ValidationError("Описание задачи должно быть длинее 100 символов")
        return description
