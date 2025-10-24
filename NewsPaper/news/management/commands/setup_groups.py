from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news.models import Post


class Command(BaseCommand):
    help = 'Создает группы common и authors'

    def handle(self, *args, **options):
        # Группа common
        common_group, created = Group.objects.get_or_create(name='common')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа common создана'))
        else:
            self.stdout.write(self.style.WARNING('Группа common уже существует'))

        # Группа authors с правами
        authors_group, created = Group.objects.get_or_create(name='authors')

        # Права для модели Post
        content_type = ContentType.objects.get_for_model(Post)

        add_permission = Permission.objects.get(codename='add_post', content_type=content_type)
        change_permission = Permission.objects.get(codename='change_post', content_type=content_type)

        authors_group.permissions.add(add_permission, change_permission)
        authors_group.save()

        self.stdout.write(self.style.SUCCESS('Группа authors создана с правами на создание и редактирование постов'))