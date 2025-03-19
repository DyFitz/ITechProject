from django.db.models.signals import post_migrate, post_save
from django.contrib.auth.models import Group, Permission, User
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Profile


@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    # Only run for our app
    if sender.name == 'srcweb':
        # Get the ContentType for the Event model
        event_ct = ContentType.objects.get(app_label='srcweb', model='event')

        # Create or update the Events Coordinator group
        coordinator_group, created = Group.objects.get_or_create(name='Events Coordinator')
        # Grant all permissions (add, change, delete, view) on the Event model
        perms = Permission.objects.filter(content_type=event_ct)
        coordinator_group.permissions.set(perms)

        # Create or update the Student group
        student_group, created = Group.objects.get_or_create(name='Student')
        # Grant only the view permission for the Event model (optional)
        view_permission = Permission.objects.get(content_type=event_ct, codename='view_event')
        student_group.permissions.set([view_permission])


@receiver(post_save, sender=User)
def assign_user_to_group(sender, instance, created, **kwargs):
    if created:
        # Ensure the user has an associated Profile
        if hasattr(instance, 'profile'):
            if instance.profile.user_type == 'coordinator':
                group = Group.objects.get(name='Events Coordinator')
            else:
                group = Group.objects.get(name='Student')
            instance.groups.add(group)
