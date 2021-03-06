from django.urls import path

from TODO_list.views.project_views import IndexProjectView, DetailProjectView, CreateProjectView
from TODO_list.views.tasks_views import IndexView, TaskView, CreateTask, DeleteTask, UpdateTask

urlpatterns = [
    # path('', IndexView.as_view(), name='index'),
    path('', IndexProjectView.as_view(), name='list_project_view'),
    path('project/<int:pk>/project/view', DetailProjectView.as_view(), name='detail_project_view'),
    path('project/create/', CreateProjectView.as_view(), name='create_project'),
    path('task/<int:pk>/view/', TaskView.as_view(), name='view'),
    path('task/create/', CreateTask.as_view(), name='create'),
    path('task/<int:pk>/delete', DeleteTask.as_view(), name='delete'),
    path('task/<int:pk>/update', UpdateTask.as_view(), name='update'),
    path('project/view/', IndexProjectView.as_view(), name='index_project_view')
]
