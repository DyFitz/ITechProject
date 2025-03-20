from django.db.models.signals import post_migrate, post_save
from django.contrib.auth.models import Group, Permission, User
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Profile


# Signal triggered after database migrations to create user groups with permissions
@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    if sender.name == 'srcweb':
        event_ct = ContentType.objects.get(app_label='srcweb', model='event')

        # Creates Events Coordinator group and assigns all permissions on Event model
        coordinator_group, created = Group.objects.get_or_create(name='Events Coordinator')
        perms = Permission.objects.filter(content_type=event_ct)
        coordinator_group.permissions.set(perms)

        # Creates Student group and assigns view-only permission on Event model
        student_group, created = Group.objects.get_or_create(name='Student')
        view_permission = Permission.objects.get(content_type=event_ct, codename='view_event')
        student_group.permissions.set([view_permission])


# Automatically assigns new users to groups based on their profile user type
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from srcweb.models import Profile


@receiver(post_save, sender=Profile)
def update_user_group(sender, instance, **kwargs):
    user = instance.user
    # Clear existing groups (if you want to enforce a strict one-group policy)
    user.groups.clear()

    if instance.user_type == 'coordinator':
        group = Group.objects.get(name='Events Coordinator')
    else:
        group = Group.objects.get(name='Student')

    user.groups.add(group)
