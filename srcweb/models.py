from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail


# Profile model extending built-in User model for additional data
class Profile(models.Model):
    # Site user types
    USER_TYPES = (
        ('student', 'Student'),
        ('coordinator', 'Events Coordinator'),
    )
    # Link to built in user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='student')

    def __str__(self):
        return f"{self.user.username} ({self.get_user_type_display()})"


# Signal to automatically create or update profile when a User object is created/saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create profile if user is newly created
        Profile.objects.create(user=instance)
    instance.profile.save() # Always save profile when user is saved


# Event model representing an event
class Event(models.Model):
    title = models.CharField(max_length=255)     # Event title
    description = models.TextField()            # Detailed description of the event
    event_date = models.DateTimeField()         # Date and time of the event
    location = models.CharField(max_length=255) # Event location
    total_tickets = models.PositiveIntegerField()   # Total number of tickets available
    available_tickets = models.PositiveIntegerField()   # Tickets currently available
    # User who created the event
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    # Users attending the event
    attendees = models.ManyToManyField(User, related_name='attending_events', blank=True)

    def __str__(self):
        return self.title

    # Method to book tickets for the event
    def book_ticket(self, user):
        """
        Allow a student to book a ticket if available and if they haven't exceeded their limit.
        Sends an email confirmation to the user upon successful booking.
        """
        if self.available_tickets > 0 and self.attendees.filter(id=user.id).count() < 2:
            self.attendees.add(user)
            self.available_tickets -= 1
            self.save()

            # Send a confirmation email
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
        return False