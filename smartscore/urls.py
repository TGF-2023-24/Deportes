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
    path('advanced_search/', views.advanced_search, name='advanced_search'),
    path('search_results/', views.search_results, name='search_results'),
    path('api/position-stats/<str:position>/<int:custom_id>/', views.position_stats_api, name='position_stats_api'),
    path('my_squads/', views.my_squads, name='my_squads'),
    path('squad_builder/', views.squad_builder, name='squad_builder'),
    path('squad/<int:squad_id>/players/', views.squad_players, name='squad_players'),
    path('squad/<int:squad_id>/players/<str:position>/', views.players_by_position, name='players_by_position'),
    path('create_squad/', views.create_squad, name='create_squad'),
    path('edit_squad/<int:squad_id>/', views.edit_squad, name='edit_squad'),
    path('delete_squad/<int:squad_id>/', views.delete_squad, name='delete_squad'),
    path('add_to_squad/<int:custom_id>/', views.add_to_squad, name='add_to_squad'),
    path('api/squad-stats/<str:position>/<str:players>/', views.squad_stats_api, name='squad_stats_api'),
    path('api/replacement-players/<str:position>/<str:player>/', views.get_replacement_players, name='get_replacement_players'),
]