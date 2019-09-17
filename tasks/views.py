from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Task, Comment


class TasksListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/tasks_list.html'


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks/task_create.html'
    fields = ['description', 'status', 'users']

    def remove_archived_status_option(self, form):
        status_choices = form.fields['status'].choices
        status_choices.remove(('Archived', 'Archived'))
        form.fields['status'].choices = status_choices

    def get_form(self, form_class=None):
        form = super(TaskCreateView, self).get_form(form_class)
        if not self.request.user.groups.filter(name='Administrator').exists():
            self.remove_archived_status_option(form)
        return form


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'tasks/task_update.html'
    fields = ['description', 'status', 'users']

    def remove_archived_status_option(self, form):
        status_choices = form.fields['status'].choices
        status_choices.remove(('Archived', 'Archived'))
        form.fields['status'].choices = status_choices

    def get_form(self, form_class=None):
        form = super(TaskUpdateView, self).get_form(form_class)
        if not self.request.user.groups.filter(name='Administrator').exists():
            self.remove_archived_status_option(form)
        return form

    def form_valid(self, form):
        task_update_view = super(TaskUpdateView, self).form_valid(form)
        form.instance.notify_users()
        return task_update_view


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'tasks/comment_create.html'
    fields = ['comment']

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(Task, pk=kwargs['pk'])
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.task = self.task
        form.instance.user = self.user
        comment_create_view = super().form_valid(form)
        self.task.notify_users()
        return comment_create_view

class CommentDeleteView(UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'tasks/comment_check_delete.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Administrator').exists()

    def get_success_url(self):
        task = self.object.task
        return reverse('task_detail', args=[task.id])
