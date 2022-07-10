from django.urls import path

from TODO_list.views import IndexView, TaskView, CreateTask, DeleteTask, UpdateTask

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('task/<int:pk>/view/', TaskView.as_view(), name='view'),
    path('task/create/', CreateTask.as_view(), name='create'),
    path('task/<int:pk>/delete', DeleteTask.as_view(), name='delete'),
    path('task/<int:pk>/update', UpdateTask.as_view(), name='update')
]
