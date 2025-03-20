from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.core import mail
from datetime import datetime, timedelta

from srcweb.models import Profile, Event
from srcweb.forms import EventForm


class ProfileSignalTest(TestCase):
    def test_profile_created(self):
        """
        When a new user is created, a Profile should be automatically created.
        """
        user = User.objects.create_user(username='testuser', password='testpass')
        # Check that the profile exists and has the default user_type 'student'
        self.assertIsNotNone(user.profile)
        self.assertEqual(user.profile.user_type, 'student')

    def test_group_assignment(self):
        # Create a new user (profile defaults to 'student')
        user = User.objects.create_user(username='coordinator', password='testpass')
        # Update the profile user type to coordinator
        user.profile.user_type = 'coordinator'
        user.profile.save()
        coordinator_group = Group.objects.get(name='Events Coordinator')
        self.assertIn(coordinator_group, user.groups.all())


class EventBookTicketTest(TestCase):
    def setUp(self):
        """
        Create a user and an event instance for booking tests.
        """
        self.user = User.objects.create_user(
            username='ticketuser',
            password='testpass',
            email='ticketuser@example.com'
        )
        # Create an event with 10 tickets available
        self.event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            event_date=datetime.now() + timedelta(days=1),
            location="Test Location",
            total_tickets=10,
            available_tickets=10,
            created_by=self.user
        )

    def test_book_ticket_success(self):
        """
        Verify that booking a ticket reduces available tickets, adds the user as an attendee,
        and sends a confirmation email.
        """
        result = self.event.book_ticket(self.user)
        self.assertTrue(result)
        self.assertIn(self.user, self.event.attendees.all())
        self.assertEqual(self.event.available_tickets, 9)
        # Confirm that an email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Ticket Confirmation", mail.outbox[0].subject)

    def test_book_ticket_limit(self):
        result1 = self.event.book_ticket(self.user)
        result2 = self.event.book_ticket(self.user)
        result3 = self.event.book_ticket(self.user)
        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertFalse(result3)


class EventFormTest(TestCase):
    def test_event_form_valid_data(self):
        """
        Verify that the form is valid when all required fields are provided.
        """
        form_data = {
            'title': 'New Event',
            'description': 'Event description',
            # Use an appropriate string format for the datetime field.
            'event_date': (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"),
            'location': 'Test Location',
            'total_tickets': 100,
        }
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_event_form_missing_data(self):
        """
        Verify that the form is invalid when required fields are missing.
        """
        form_data = {
            'title': '',
            'description': 'Event description',
            # Missing event_date and location.
            'total_tickets': 100,
        }
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())
