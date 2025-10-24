from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from allauth.account.signals import user_signed_up

@receiver(post_save, sender=User)
def add_user_to_common_group(sender, instance, created, **kwargs):
    if created:
        common_group = Group.objects.get(name='common')
        instance.groups.add(common_group)

@receiver(user_signed_up)
def social_account_user_signed_up(request, user, **kwargs):
    common_group = Group.objects.get(name='common')
    user.groups.add(common_group)