from django.urls import path
from .views import home_view, like_post, like_view, delete_post, view_story, add_post, profile_view, my_videos, add_comment, following_add, followers_list, following_list, add_story

urlpatterns = [
    path('', home_view, name='home'),
    path('like/<int:id>/', like_post, name="like_post"),
    path('like_view', like_view, name='likes'),
    path('add_post', add_post, name='add'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('add_coment/<int:id>', add_comment, name='add_comment'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('followers/<int:user_id>/', followers_list, name='followers_list'),
    path('following/<int:user_id>/', following_list, name='following_list'),
    path('add_story/', add_story, name='add_story'),
    path('story/<int:story_id>/', view_story, name='view_story'),
    path('my-videos/<int:id>/', my_videos, name='my_videos'),
    path('delete-post/<int:post_id>/', delete_post, name='delete_post'),
    path('following/add/<int:user_id>/', following_add, name='following_add')
    ]   