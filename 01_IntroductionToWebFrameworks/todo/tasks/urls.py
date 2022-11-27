from django.urls import path

from .views import ToDoView

urlpatterns = [
    path('', ToDoView.as_view(), name='todo-view'),
]
