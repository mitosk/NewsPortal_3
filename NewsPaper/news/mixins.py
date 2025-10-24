from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class AuthorRequiredMixin(PermissionRequiredMixin):
    """Миксин для проверки прав автора"""
    permission_required = 'news.add_post'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm(self.permission_required):
            raise PermissionDenied("У вас нет прав для выполнения этого действия")
        return super().dispatch(request, *args, **kwargs)