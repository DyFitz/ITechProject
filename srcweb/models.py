from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

# Profile model extending built-in User model for additional data
class Profile(models.Model):
    USER_TYPES = (
        ('student', 'Student'),
        ('coordinator', 'Events Coordinator'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='student')

    def __str__(self):
        return f"{self.user.username} ({self.get_user_type_display()})"


# Signal to automatically create or update a Profile when a User is created/saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


# Event model representing an event
class Event(models.Model):
    title = models.CharField(max_length=255)                   # Event title
    description = models.TextField()                           # Event description
    event_date = models.DateTimeField()                        # Date and time of the event
    location = models.CharField(max_length=255)                # Event location
    total_tickets = models.PositiveIntegerField()              # Total tickets available
    available_tickets = models.PositiveIntegerField()          # Tickets still available
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_events'
    )
    # Use a through model (Ticket) to allow multiple tickets per user.
    attendees = models.ManyToManyField(
        User, through='Ticket', related_name='attending_events', blank=True
    )

    def book_ticket(self, user):
        """
        Allow a student to book a ticket if available and if they haven't exceeded their limit.
        Sends an email confirmation upon successful booking.
        """
        if self.available_tickets <= 0:
            return False

        # Try to retrieve an existing ticket record for this user.
        try:
            ticket = Ticket.objects.get(event=self, user=user)
        except Ticket.DoesNotExist:
            ticket = None

        if ticket:
            if ticket.quantity >= 2:
                return False
            ticket.quantity += 1
            ticket.save()
        else:
            ticket = Ticket.objects.create(event=self, user=user, quantity=1)

        self.available_tickets -= 1
        self.save()

        # Send confirmation email
        send_mail(
            subject=f'Ticket Confirmation for {self.title}',
            message=(
                f'Dear {user.username},\n\n'
                f'Your ticket for the event "{self.title}" has been confirmed.\n\n'
                f'Event Details:\n'
                f'Description: {self.description}\n'
                f'Date: {self.event_date}\n'
                f'Location: {self.location}\n\n'
                f'Thank you for booking with us.'
            ),
            from_email='src-no-reply@protonmail.com',
            recipient_list=[user.email],
            fail_silently=False,
        )
        return True

    def __str__(self):
        return self.title


# Ticket model to track ticket bookings per user per event.
class Ticket(models.Model):
    # Use a string reference for Event to avoid ordering issues.
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.quantity})"
