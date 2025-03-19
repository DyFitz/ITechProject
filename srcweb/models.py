from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail


# Profile model extending the default User model.
class Profile(models.Model):
    USER_TYPES = (
        ('student', 'Student'),
        ('coordinator', 'Events Coordinator'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='student')

    def __str__(self):
        return f"{self.user.username} ({self.get_user_type_display()})"


# Signal to automatically create or update a Profile when a User is saved.
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    total_tickets = models.PositiveIntegerField()
    available_tickets = models.PositiveIntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    attendees = models.ManyToManyField(User, related_name='attending_events', blank=True)

    def __str__(self):
        return self.title

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
                from_email='noreply@example.com',  # Replace with your sending email address
                recipient_list=[user.email],
                fail_silently=False,
            )
            return True
        return False