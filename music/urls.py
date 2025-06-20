from django.urls import path
from . import views

urlpatterns = [
    path('', views.userlogin, name='login'),
    path('register/', views.register, name='register'),
    path('authority/', views.manage_roles, name='authority'),
    path('logout/', views.logoutnows, name='logout'),
    path('no-permission/', views.no_permission, name='no_permission'),

    path('musics/', views.index, name='index'),
    path('music/<int:id>/', views.view_music, name='view_music'),
    path('music/add/', views.add, name='add'),
    path('music/edit/<int:id>/', views.edit, name='edit'),
    path('music/delete/<int:id>/', views.delete, name='delete'),
    
    path('artists/', views.artist_index, name='artist_index'),
    path('artist/<int:id>/', views.view_artist, name='view_artist'),
    path('artist/add/', views.add_artist, name='add_artist'),
    path('artist/edit/<int:id>/', views.edit_artist, name='edit_artist'),
    path('artist/delete/<int:id>/', views.delete_artist, name='delete_artist'),
    
    path('albums/', views.album_index, name='album_index'),
    path('album/<int:id>/', views.view_album, name='view_album'),
    path('album/add/', views.add_album, name='add_album'),
    path('album/edit/<int:id>/', views.edit_album, name='edit_album'),
    path('album/delete/<int:id>/', views.delete_album, name='delete_album'),

    path('prices/', views.price_index, name='price_index'),
    path('price/<int:id>/', views.view_price, name='view_price'),
    path('price/add/', views.add_price, name='add_price'),
    path('price/edit/<int:id>/', views.edit_price, name='edit_price'),
    path('price/delete/<int:id>/', views.delete_price, name='delete_price'),

    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/delete/', views.delete_account, name='delete_account'),
    
]
