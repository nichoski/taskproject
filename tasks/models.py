from django.db import models
from django.contrib.auth.models import User, Group
from django.core.mail import send_mass_mail
from django.urls import reverse

class Task(models.Model):
    description = models.TextField()
    users = models.ManyToManyField(User, blank=True)
    STATUS_CHOICES = (
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Archived', 'Archived'),
    )
    status = models.CharField(max_length=11, default='New', choices=STATUS_CHOICES)

    def get_absolute_url(self):
        return reverse('task_detail', args=[self.id])

    def notify_users(self):
        messages_list = []
        for user in self.users.exclude(email=''):
            messages_list.append(self.prepare_notification_message(user))
        messages = tuple(messages_list)
        if messages:
            send_mass_mail(messages)

    def prepare_notification_message(self, user):
        task_id = str(self.id)
        subject = 'Task {} requires your attention'.format(task_id)
        body = 'Updates were made to task {}.'.format(task_id)
        from_email = 'noreply@taskproject.com'
        recipient_list = [user.email]
        return subject, body, from_email, recipient_list


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment = models.TextField()

    def get_absolute_url(self):
        return reverse('task_detail', args=[self.task.id])

