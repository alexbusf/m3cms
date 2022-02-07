from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns =[
    path('accounts/login/', views.UserLogin.as_view(), name="login"),
    path('accounts/logout/', LogoutView.as_view(), name="logout"),
    path('', views.PostListView.as_view(), name='post-list'),
    path('search/', views.SearchResultsView.as_view(), name='search-results'),
    path('category/<slug:category_slug>/', views.PostByCategoryView.as_view(), name='post-by-category'),
    path('author/<int:pk>/', views.PostByAuthorView.as_view(), name='post-by-author'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='new-post'),
    path('post/<slug:slug>/update', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<slug:slug>/delete', views.PostDeleteView.as_view(), name='post-delete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)