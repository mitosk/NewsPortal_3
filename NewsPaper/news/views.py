from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from .models import Post, Category, Author
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.exceptions import PermissionDenied


@login_required
def become_author(request):
    if request.method == 'POST':
        authors_group = Group.objects.get(name='authors')
        request.user.groups.add(authors_group)
        messages.success(request, 'Поздравляем! Теперь вы автор и можете создавать и редактировать посты.')
        return redirect('/news/')

    return render(request, 'news/become_author.html')


# Простые функциональные представления для основной страницы
def news_list(request):
    """Простое представление для списка всех постов"""
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'news/news_list.html', {'posts': posts})


def news_detail(request, pk):
    """Простое представление для деталей поста"""
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'news/news_detail.html', {'post': post})


# Существующие классовые представления (оставляем как есть)
class NewsList(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        return Post.objects.filter(post_type='news')


class ArticleList(ListView):
    model = Post
    template_name = 'news/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        return Post.objects.filter(post_type='article')


class NewsSearch(ListView):
    model = Post
    template_name = 'news/news_search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(post_type='news').order_by('-created_at')
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ArticleSearch(ListView):
    model = Post
    template_name = 'news/article_search.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(post_type='article').order_by('-created_at')
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


# Обновляем представления создания с проверкой прав
class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/news_edit.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'news'

        # Автоматически устанавливаем автора
        try:
            # Пытаемся получить автора по умолчанию
            from django.contrib.auth.models import User
            user = User.objects.get(username='default_author')
            author = Author.objects.get(user=user)
            post.author = author
        except (User.DoesNotExist, Author.DoesNotExist):
            # Если автора по умолчанию нет, берем первого существующего
            author = Author.objects.first()
            if author:
                post.author = author
            else:
                # Если вообще нет авторов, создаем нового
                user = User.objects.create_user(
                    username='auto_author',
                    first_name='Автоматический',
                    last_name='Автор'
                )
                author = Author.objects.create(user=user)
                post.author = author

        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/news_edit.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.change_post'

    def get_queryset(self):
        return Post.objects.filter(post_type='news')


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.delete_post'

    def get_queryset(self):
        return Post.objects.filter(post_type='news')


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/article_edit.html'
    success_url = reverse_lazy('article_list')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.post_type = 'article'

        # Та же логика для статей
        try:
            from django.contrib.auth.models import User
            user = User.objects.get(username='default_author')
            author = Author.objects.get(user=user)
            article.author = author
        except (User.DoesNotExist, Author.DoesNotExist):
            author = Author.objects.first()
            if author:
                article.author = author
            else:
                user = User.objects.create_user(
                    username='auto_author',
                    first_name='Автоматический',
                    last_name='Автор'
                )
                author = Author.objects.create(user=user)
                article.author = author

        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/article_edit.html'
    success_url = reverse_lazy('article_list')
    permission_required = 'news.change_post'

    def get_queryset(self):
        return Post.objects.filter(post_type='article')


class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/article_delete.html'
    success_url = reverse_lazy('article_list')
    permission_required = 'news.delete_post'

    def get_queryset(self):
        return Post.objects.filter(post_type='article')


# Альтернативные представления (используют ID вместо slug)
class NewsByCategory(ListView):
    model = Post
    template_name = 'news/news_by_category.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return Post.objects.filter(
            post_type='news',
            categories=self.category
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ArticlesByCategory(ListView):
    model = Post
    template_name = 'news/articles_by_category.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return Post.objects.filter(
            post_type='article',
            categories=self.category
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class CategoryList(ListView):
    model = Category
    template_name = 'news/category_list.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Вручную считаем количество постов для каждой категории
        categories_with_counts = []
        total_news = 0
        total_articles = 0

        for category in context['categories']:
            news_count = Post.objects.filter(
                post_type='news',
                categories=category
            ).count()
            articles_count = Post.objects.filter(
                post_type='article',
                categories=category
            ).count()

            categories_with_counts.append({
                'category': category,
                'news_count': news_count,
                'articles_count': articles_count
            })

            total_news += news_count
            total_articles += articles_count

        context['categories_with_counts'] = categories_with_counts
        context['total_news'] = total_news
        context['total_articles'] = total_articles
        return context


# Убираем вложенные классы и выносим их отдельно
class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'text', 'category', 'post_type']
    template_name = 'news/post_edit.html'
    success_url = '/news/'
    permission_required = 'news.add_post'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'text', 'category', 'post_type']
    template_name = 'news/post_edit.html'
    success_url = '/news/'
    permission_required = 'news.change_post'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied("Вы можете редактировать только свои посты")
        return super().dispatch(request, *args, **kwargs)