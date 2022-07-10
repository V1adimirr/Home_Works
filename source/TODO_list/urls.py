from django.urls import path

from TODO_list.views import IndexView, TaskView, CreateTask

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('task/<int:pk>/view/', TaskView.as_view(), name='view'),
    path('task/create/', CreateTask.as_view(), name='create'),
]
