from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup_user, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('player/<int:custom_id>/', views.player_detail, name='player_detail'),
    path('search_player/', views.search_player, name='search_player'),
]