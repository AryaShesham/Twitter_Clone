# import the below mentioned things to create a Url-Pattern for the view that is created
from django.urls import path
from .views import PostDetailView, PostListView, PostEditView, PostDeleteView, CommentDeleteView, ProfileEditView, ProfileView, AddFollower, RemoveFollower, AddLike, UserSearch, ListOfFollowers, AddCommentLike, CommentReplyView

# url-pattern list:

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/edit/<int:pk>/', PostEditView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/',
         CommentDeleteView.as_view(), name='comment-delete'),
    path('post/<int:post_pk>/comment/<int:pk>/like',
         AddCommentLike.as_view(), name='comment-like'),
    path('post/<int:post_pk>/comment/<int:pk>/reply',
         CommentReplyView.as_view(), name='comment-reply'),
    path('post/<int:pk>/like', AddLike.as_view(), name='like'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='profile-edit'),
    path('profile/<int:pk>/followers/add',
         AddFollower.as_view(), name='add-follower'),
    path('profile/<int:pk>/followers/remove',
         RemoveFollower.as_view(), name='remove-follower'),
    path('search/', UserSearch.as_view(), name='profile-search'),
    path('profile/<int:pk>/followers',
         ListOfFollowers.as_view(), name='followers-list'),
]
