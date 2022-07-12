from django import forms
from django.forms import widgets

from TODO_list.models import Type, Status


class TaskForm(forms.Form):
    short_de = forms.CharField(max_length=100, required=True, label='Краткое описание')
    description = forms.CharField(max_length=2000, required=False,
                                  widget=widgets.Textarea(attrs={"cols": 20, "rows": 6}), label='Описание')
    status = forms.ModelChoiceField(queryset=Status.objects.all())
    types = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), widget=forms.CheckboxSelectMultiple)
