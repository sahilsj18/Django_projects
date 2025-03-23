from django.urls import path
from .views import task_list, task_detail

urlpatterns = [
    path('api/tasks/', task_list, name='task_list_api'),
    path('api/tasks/<int:id>/', task_detail, name='task_detail_api'),
]
