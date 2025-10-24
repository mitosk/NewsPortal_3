from django.urls import path
from django.urls import path, include
from . import views
from .views import (
    NewsList, ArticleList, NewsSearch, ArticleSearch,
    NewsCreate, NewsUpdate, NewsDelete,
    ArticleCreate, ArticleUpdate, ArticleDelete,
    NewsByCategory, ArticlesByCategory, CategoryList  # ← ВАЖНО: добавить эти три класса
)

urlpatterns = [
    # Основные страницы
    path('news/', NewsList.as_view(), name='news_list'),
    path('articles/', ArticleList.as_view(), name='article_list'),

    # Поиск и фильтрация
    path('news/search/', NewsSearch.as_view(), name='news_search'),
    path('articles/search/', ArticleSearch.as_view(), name='article_search'),

    # Фильтрация по категориям
    path('categories/', CategoryList.as_view(), name='category_list'),
    path('news/category/<int:category_id>/', NewsByCategory.as_view(), name='news_by_category'),
    path('articles/category/<int:category_id>/', ArticlesByCategory.as_view(), name='articles_by_category'),

    # Создание, редактирование, удаление новостей
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

    # Создание, редактирование, удаление статей
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('accounts/', include('allauth.urls')),
    path('become-author/', views.become_author, name='become_author'),
]