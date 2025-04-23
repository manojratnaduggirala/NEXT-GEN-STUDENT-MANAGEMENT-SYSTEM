from django.test import TestCase, Client
from django.urls import reverse
from next_gen_sms.models import CustomUser
from next_gen_sms.models import Event

class EventViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = CustomUser.objects.create_superuser(
            username='admin',
            password='testpass123',
            email='admin@example.com',
            role='admin'
        )
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            date='2025-01-01',
            time='10:00:00'
        )

    def test_events_list_view(self):
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('next_gen_sms:events_list'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Event')
        self.assertTemplateUsed(response, 'events/events_list.html')

    def test_add_event_view_authenticated(self):
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('next_gen_sms:add_event'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/add_event.html')

    def test_edit_event_view_authenticated(self):
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('next_gen_sms:edit_event', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/edit_event.html')

    def test_delete_event_view(self):
        self.client.login(username='admin', password='testpass123')
        response = self.client.post(reverse('next_gen_sms:delete_event', args=[self.event.id]), follow=True)
        self.assertEqual(response.status_code, 200)  # After following redirect
        self.assertEqual(Event.objects.count(), 0)
