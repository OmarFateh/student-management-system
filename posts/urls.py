from django.urls import path

from .views import (
    # post
    post_detail,
    add_post,
    update_post,
    delete_post,
    delete_post_detail,
    # comments
    update_comment,
    delete_comment,
    comment_likes,
    CommentLikeAPIToggle,
    # likes
    post_likes,
    PostLikeAPIToggle,
)

# namespace = posts 

urlpatterns = [
    # post
    path('p/<str:post_slug>/', post_detail, name='post-detail'),
    path('p/ajax/add/', add_post, name='add-post'),
    path('p/<str:post_slug>/update/', update_post, name='update-post'),
    path('p/<str:post_slug>/delete/', delete_post, name='delete-post'),
    path('p/<str:post_slug>/detail/delete/', delete_post_detail, name='delete-post-detail'),

    # comments
    path('c/<int:comment_id>/ucdate/', update_comment, name='update-comment'),
    path('c/<int:comment_id>/delete/', delete_comment, name='delete-comment'),
    path('c/<int:comment_id>/likes/', comment_likes, name='comment-likes'),
    path('api/c/<int:comment_id>/like/', CommentLikeAPIToggle.as_view(), name='comment-like-api-toggle'),

    # likes
    path('p/<str:post_slug>/likes/', post_likes, name='post-likes'),
    path('api/p/<str:post_slug>/like/', PostLikeAPIToggle.as_view(), name='post-like-api-toggle'),
]