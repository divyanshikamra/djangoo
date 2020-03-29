from django.urls import path
from . import views

urlpatterns = [
    path('',views.articles_list,name="list"),
    path('loggedin',views.logged_in, name="loggedin"),
    path('create',views.article_create, name="create"),
    path('<slug:slog>/edit/', views.edit_post, name="edit"),
    path('<slug:slog>/delete/', views.delete_post, name="delete"),
    path('<str:slog>/', views.article_detail, name="detail"),
]
