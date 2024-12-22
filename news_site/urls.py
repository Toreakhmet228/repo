from news.views import *
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', NewsListView.as_view(), name='news-list'),
    path('news/<str:category_name>/', NewsByCategoryView.as_view(), name='news-by-category'),
    path('news/comment/add/', AddCommentView.as_view(), name='add_comment'),
        path('news/<int:news_id>/like/', LikeNewsView.as_view(), name='like_news'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
