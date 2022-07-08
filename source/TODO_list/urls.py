from django.urls import path

from TODO_list.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index')
]