from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task, Comment

# Create your tests here.
class SampleTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="User1")
        self.admin_user = User.objects.create(username="AdminUser")
        self.admin_user.groups.create(name='Administrator')
        self.first_task = Task.objects.create(description='First task.', status='New')
        self.first_comment = self.first_task.comment_set.create(user=self.user, comment='First comment.')

    def test_anonymous_user_access(self):
        # Listing tasks
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 302)
        # New task GET request
        response = self.client.get(reverse('add_task'))
        self.assertEqual(response.status_code, 302)
        # New task POST request
        response = self.client.post(reverse('add_task'))
        self.assertEqual(response.status_code, 302)

    def test_tasks_list_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)

    def test_task_create_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('add_task'))
        self.assertEqual(response.status_code, 200)

    def test_task_create_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('add_task'), {'description':'Asdf', 'status':'New'})
        self.assertEqual(response.status_code, 302)

    def test_task_create_post_bad_data(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('add_task'), {'status':'Asdf'})
        self.assertEqual(response.status_code, 200)

    def test_task_detail(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('task_detail', args=[self.first_task.id]))
        self.assertEqual(response.status_code, 200)

    def test_task_update_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('task_update', args=[self.first_task.id]))
        self.assertEqual(response.status_code, 200)

    def test_task_update_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('task_update', args=[self.first_task.id]), {'status':'New', 'description':'asdf'})
        self.assertEqual(response.status_code, 302)

    def test_task_update_post_bad_data(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('task_update', args=[self.first_task.id]), {'status':''})
        self.assertEqual(response.status_code, 200)

    def test_task_update_post_archive_by_admin(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(reverse('task_update', args=[self.first_task.id]), {'status':'Archived', 'description':'asdf'})
        self.assertEqual(response.status_code, 302)

    def test_task_update_post_archive_by_non_admin(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('task_update', args=[self.first_task.id]), {'status':'Archived', 'description':'asdf'})
        self.assertEqual(response.status_code, 200)

    def test_comment_create_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('add_comment', args=[self.first_task.id]))
        self.assertEqual(response.status_code, 200)

    def test_comment_create_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('add_comment', args=[self.first_task.id]), {'comment':'Comment text.'})
        self.assertEqual(response.status_code, 302)

    def test_comment_create_post_bad_data(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('add_comment', args=[self.first_task.id]), {'comment':''})
        self.assertEqual(response.status_code, 200)

    def test_comment_delete_by_admin(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(reverse('delete_comment', args=[self.first_comment.id]))
        self.assertEqual(response.status_code, 302)

    def test_comment_delete_by_non_admin(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete_comment', args=[self.first_comment.id]))
        self.assertEqual(response.status_code, 403)

