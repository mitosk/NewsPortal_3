from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news.models import Post


# Создание групп и назначение прав
def setup_groups():
    # Группа common - базовые права
    common_group, created = Group.objects.get_or_create(name='common')

    # Группа authors - права на создание и редактирование постов
    authors_group, created = Group.objects.get_or_create(name='authors')

    # Получаем права для модели Post
    content_type = ContentType.objects.get_for_model(Post)
    post_permissions = Permission.objects.filter(content_type=content_type)

    # Добавляем права на создание и изменение постов для authors
    add_permission = Permission.objects.get(codename='add_post', content_type=content_type)
    change_permission = Permission.objects.get(codename='change_post', content_type=content_type)

    authors_group.permissions.add(add_permission, change_permission)
    authors_group.save()


# Вызываем функцию при запуске админки
setup_groups()