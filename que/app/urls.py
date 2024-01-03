# yourappname/urls.py

from django.urls import path
from .views import home, register, user_login,edit_profile,ProfileUpdateView,user_logout,view_profile
from .views import create_post, view_post, add_comment, like_post,all_posts,index,friend_request,accept_friend_request,user_detail,friend_profile,search_users
from django.views.generic import TemplateView







urlpatterns = [
    path('', home, name='home'),
    path('user/<str:username>/', user_detail, name='user_detail'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('create_post/', create_post, name='create_post'),
    path('view_post/<int:post_id>/', view_post, name='view_post'),
    path('add_comment/<int:post_id>/', add_comment, name='add_comment'),
    path('like_post/<int:post_id>/', like_post, name='like_post'),
    path('all_posts/', all_posts, name='allposts'),  # Add this URL for all posts
    path('index/', index, name='index'),  # Add this URL for all posts
    path('friend-request/<str:username>/', friend_request, name='friend_request'),
    path('accept-friend-request/<int:friendship_id>/', accept_friend_request, name='accept_friend_request'),
    path('friend/<int:friend_id>/', friend_profile, name='friend_profile'),
    path('search-users/', search_users, name='search_users'),
    path('profile/', view_profile, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='edit_profile_cbv'),



    
    # Add other URLs as needed
    # Add other URL patterns as needed
]
# Add the WebSocket URL patterns to the main urlpatterns
