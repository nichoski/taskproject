from django.urls import path

from . import views

urlpatterns = [
    path('', views.TasksListView.as_view(), name='tasks'),
    path('add', views.TaskCreateView.as_view(), name='add_task'),
    path('task/<int:pk>', views.TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:pk>/update', views.TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/add-comment', views.CommentCreateView.as_view(), name='add_comment'),
    path('comment/<int:pk>/delete', views.CommentDeleteView.as_view(), name='delete_comment'),
]
