from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from feed.staff.views import staff_posts
from feed.student.views import student_posts
from notifications.models import Notification 
from .models import Post, Comment
from .forms import PostForm, CommentForm

User = get_user_model()


@csrf_exempt
def post_detail(request, post_slug=None):
    """
    Take slug, get the post with this slug, and display the post detail.
    Create comment or reply to this post.
    """
    # get post by its slug.
    post = get_object_or_404(Post, slug=post_slug)
    # get post likes count.
    likes_count = post.likes.count()
    # check if the post is liked by the current user or not. 
    is_liked_user = False
    if request.user in post.likes.all():
        is_liked_user = True 
    # add comment.
    data = dict()
    # comment form.
    comment_form = CommentForm(request.POST or None)  
    if request.is_ajax():
        # check if the comment form is valid.
        if comment_form.is_valid():
            data['form_is_valid'] = True
            # Get data from the submitted form.
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            reply = None
            # check if it's a comment or a reply to a comment.
            if reply_id:
                # get the id of the comment to add the reply to it.
                reply = get_object_or_404(Comment, pk=reply_id)
            # create comment for this item with requested user as an owner. 
            comment = Comment.objects.create(user=request.user, post=post, reply=reply, content=content)    
        context = {"post":post, 'comment_form':comment_form, 'request':request}
        data['html_comment_list'] = render_to_string('posts/includes/partial_comment_list.html', context)
        data['html_comment_count'] = render_to_string('posts/includes/partial_comment_count.html', {"post":post})
        return JsonResponse(data)    
    context = {"post":post, 'likes_count':likes_count, 'is_liked_user':is_liked_user, 'comment_form':comment_form}
    return render(request, 'posts/post_detail.html', context)

def add_post(request):
    """
    Add new post.
    """
    data = dict()
    # check if the request method is post.
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            # add new post.
            form = post_form.save(commit=False)
            form.user = request.user
            form.save()
            data["form_is_valid"] = True
            data["is_add"] = True
            if request.user.staff:
                posts = staff_posts(request)
            elif request.user.student:
                posts = student_posts(request)
            # comment form.
            comment_form = CommentForm(auto_id=False)         
            context = {"posts":posts, "request":request, "comment_form":comment_form}
            data["html_post_list"] = render_to_string("posts/includes/partial_post_list.html", context)
        else:
            data["form_is_valid"] = False
    else:
        post_form = PostForm()
    context = {"form":post_form}
    data["html_form"] = render_to_string("posts/includes/partial_post_add.html", context, request=request)    
    return JsonResponse(data)               

def update_post(request, post_slug=None):
    """
    Take slug, get the post with this slug, and update the post.
    """
    # get post by its slug.
    post = get_object_or_404(Post, slug=post_slug)
    data = dict()
    data["is_update"] = True
    # check if the request method is post.
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES, instance=post)
        if post_form.is_valid():
            # update post.
            post_form.save()
            data["form_is_valid"] = True
            if request.user.staff:
                posts = staff_posts(request)
            elif request.user.student:
                posts = student_posts(request)
            # comment form.
            comment_form = CommentForm(auto_id=False)        
            context = {'posts':posts, 'request':request, "comment_form":comment_form}
            data["html_post_list"] = render_to_string('posts/includes/partial_post_list.html', context)
            data["html_post_detail"] = render_to_string('posts/includes/partial_post_detail.html', {'post':post, 'request':request})
        else:
            data["form_is_valid"] = False 
    else:
        post_form = PostForm(instance=post)
    context = {"post": post, "form":post_form}
    data["html_form"] = render_to_string('posts/includes/partial_post_update.html', context, request=request)    
    return JsonResponse(data)               

def delete_post(request, post_slug=None):
    """
    Take slug, get the post with this slug, and delete the post.
    """
    # get post by its slug.
    post = get_object_or_404(Post, slug=post_slug)
    data = dict()
    if request.method == 'POST':
        # delete post.
        post.delete()
        data['form_is_valid'] = True 
        data['is_update'] = False 
        if request.user.staff:
            posts = staff_posts(request)
        elif request.user.student:
            posts = student_posts(request)
        # comment form.
        comment_form = CommentForm(auto_id=False)        
        context = {'posts':posts, 'request':request, "comment_form":comment_form}
        data['html_post_list'] = render_to_string('posts/includes/partial_post_list.html', context)
    else:
        context = {'post': post}
        data['html_form'] = render_to_string('posts/includes/partial_post_delete.html', context, request=request)
    return JsonResponse(data)

def delete_post_detail(request, post_slug=None):
    """
    Take slug, get the post with this slug from post detail page.
    Delete the post, and reverse to user's profile.
    """
    # get post by its slug.
    post = get_object_or_404(Post, slug=post_slug)
    data = dict()
    if request.method == 'POST':
        # delete post.
        post.delete()
        data['form_is_valid'] = True 
        data['is_update'] = False
    else:
        context = {'post': post}
        data['html_form'] = render_to_string('posts/includes/partial_post_delete.html', context, request=request)
    return JsonResponse(data)

def update_comment(request, comment_id=None):
    """
    Take id, get the comment with this id, and update the comment.
    """
    # get comment by its id. 
    comment = get_object_or_404(Comment, pk=comment_id)
    data = dict()
    data['is_update'] = True
    # check if the request method is post.
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            # update comment.
            comment_form.save()
            data['form_is_valid'] = True
            # get comment's post.
            post = get_object_or_404(Post, pk=comment.post.id)
            context = {'post':post, 'request':request}
            data['html_comment_list'] = render_to_string('posts/includes/partial_comment_list.html', context)
        else:
            data['form_is_valid'] = False 
    else:
        comment_form = CommentForm(instance=comment)
    context = {'comment': comment, 'comment_form':comment_form}
    data['html_form'] = render_to_string('posts/includes/partial_comment_update.html', context, request=request)
    return JsonResponse(data)            

def delete_comment(request, comment_id=None):
    """
    Take id, get the comment with this id, and delete the comment.
    """
    # get comment by its id. 
    comment = get_object_or_404(Comment, pk=comment_id)
    data = dict()
    if request.method == 'POST':
        # delete comment.
        comment.delete()
        data['form_is_valid'] = True 
        data['is_update'] = False 
        # get comment's post.
        post = get_object_or_404(Post, pk=comment.post.id)
        # get post comments count.
        comments_count = post.comments.count()   
        context = {'post':post, 'request':request}
        data['html_comment_list'] = render_to_string('posts/includes/partial_comment_list.html', context)
        data['html_comment_count'] = render_to_string('posts/includes/partial_comment_count.html', {'comments_count':comments_count})
    else:
        context = {'comment': comment}
        data['html_form'] = render_to_string('posts/includes/partial_comment_delete.html', context, request=request)
    return JsonResponse(data)

def comment_likes(request, comment_id=None):
    """
    Take id, get the comment with this id, and display the comment's likes.
    """
    # get comment by its id. 
    comment = get_object_or_404(Comment, pk=comment_id)
    # get comment likes.
    data = dict()
    likes_qs = comment.likes.all()
    # get comment likes count.
    likes_count = likes_qs.count()
    context = {'likes':likes_qs, 'likes_count':likes_count}
    data['html_likes_list'] = render_to_string('posts/includes/partial_post_likes_list.html', context, request=request)
    return JsonResponse(data) 

def post_likes(request, post_slug=None):
    """
    Take slug, get the post with this slug, and display the post's likes.
    """
    # get post by its slug.
    post = get_object_or_404(Post, slug=post_slug)
    # get post likes.
    data = dict()
    likes_qs = post.likes.all()
    # get post likes count.
    likes_count = likes_qs.count()
    context = {'likes':likes_qs, 'likes_count':likes_count}
    data['html_likes_list'] = render_to_string('posts/includes/partial_post_likes_list.html', context, request=request)
    return JsonResponse(data) 

class PostLikeAPIToggle(APIView):
    """
    Post Like Toggle View.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, post_slug=None, format=None):
        """
        Take slug, get post of this slug, and add or remove user to or from the post likes' list.
        Create like notification if user liked the post, and delete like notification if user unliked the post.  
        """
        # get post by its slug.
        post = get_object_or_404(Post, slug=post_slug)
        # get current user.
        user = request.user
        updated = False
        liked = False
        # check if requested user is authenticated or not.
        if user.is_authenticated:
            # if the user has already liked this item.
            if user in post.likes.all():
                liked = False
                # remove user from item's likes.
                post.likes.remove(user)
                # if current user is not the post's owner.
                if user != post.user:
                    # set the post like notification to be inactive.
                    Notification.objects.set_inactive(sender=user, receiver=post.user, notification_type='like', post=post)
            # if not.    
            else:
                liked = True
                # add user to item's likes.
                post.likes.add(user)
                # if current user is not the post's owner.
                if user != post.user:
                    # create a like notification for this post with user as a sender, and post's owner as a receiver.  
                    Notification.objects.create(sender=user, receiver=post.user, post=post, notification_type='like') 
            updated = True
        # get likes count of this item.    
        likes_count = post.likes.count()
        data = dict()
        data['updated'] = updated
        data['liked'] = liked
        data['likes_count'] = likes_count
        return Response(data)


class CommentLikeAPIToggle(APIView):
    """
    Comment Like Toggle View.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, comment_id=None, format=None):
        """
        Take id, get comment of this id, and add or remove user to or from the comment likes' list.
        Create like comment notification if user liked the comment,
        delete like comment notification if user unliked the comment.
        """
        # get comment by its id.
        comment = get_object_or_404(Comment, pk=comment_id)
        # get current user.
        user = request.user
        updated = False
        liked = False
        # check if requested user is authenticated or not.
        if user.is_authenticated:
            # if the user has already liked this comment.
            if user in comment.likes.all():
                liked = False
                # remove user from comment's likes. 
                comment.likes.remove(user)
                # if current user is not the comment's owner.
                if user != comment.user:
                    # set the comment like notification to be inactive.
                    Notification.objects.set_inactive(sender=user, receiver=comment.user, 
                            notification_type='comment_like', post=comment.post, comment=comment)
            # if not.
            else:
                liked = True
                # add user to comment's likes. 
                comment.likes.add(user)
                # if current user is not the comment's owner.
                if user != comment.user:
                    # create like comment notification for this comment with user as a sender, comment's owner as a receiver, and comment's item as a item.
                    Notification.objects.create(sender=user, receiver=comment.user, 
                                        post=comment.post, comment=comment, notification_type='comment_like') 
            updated = True
        # get likes count of this comment.    
        comment_likes_count = comment.likes.count()
        data = dict()
        data['updated'] = updated
        data['liked'] = liked
        data['likes_count'] = comment_likes_count
        return Response(data)