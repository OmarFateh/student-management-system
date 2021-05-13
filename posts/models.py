from django.db import models
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


def post_image(instance, filename):
    """
    Upload the post image into the path and return the uploaded image path.
    """
    if instance.user.user_type == 'STAFF':
        profile_pic_path = f'staff/{instance.user.full_name}/posts/{filename}'
    elif instance.user.user_type == 'STUDENT': 
        profile_pic_path = f'student/{instance.user.full_name}/posts/{filename}'   
    return profile_pic_path


class PostAbstractRelationship(models.Model):
    """
    A abstract relationship model to inherit from.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class PostLike(PostAbstractRelationship):
    """
    A relationship model between the Post and its likes.
    """
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


class PostManager(models.Manager):
    """
    Override the post manager.
    """
    def feed(self, students_ids_list, staff_ids_list):
        """
        """
        return self.get_queryset().filter(
            Q(user__id__in=students_ids_list)|
            Q(user__id__in=staff_ids_list)
        ).distinct().order_by('-created_at')

    def parent_comments(self):
        """
        Get all parent comments of a post.
        """ 
        return Comment.objects.filter_by_parent(self)         


class Post(models.Model):
    """
    Post model.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    slug = models.CharField(max_length=10, unique=True, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=post_image, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True, through=PostLike)
    restrict_comment = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PostManager()
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        # Return post id and user's full name.
        return f"{self.id} | {str(self.user.full_name)}"

    def get_absolute_url(self):
        # Return absolute url of post by its slug.
        return reverse('posts:post-detail', kwargs={'post_slug': self.slug})    

    def get_update_absolute_url(self):
        # Return absolute url of update post by its slug.
        return reverse('posts:update-post', kwargs={'post_slug': self.slug}) 

    def get_delete_absolute_url(self):
        # Return absolute url of delete post by its slug.
        return reverse('posts:delete-post', kwargs={'post_slug': self.slug})

    def get_delete_detail_absolute_url(self):
        # Return absolute url of delete post detail by its slug.
        return reverse('posts:delete-post-detail', kwargs={'post_slug': self.slug})

    def get_post_likes_absolute_url(self):
        # Return absolute url of post's likes by its slug.
        return reverse('posts:post-likes', kwargs={'post_slug': self.slug})             

    def get_api_like_url(self):
        # Return api url of the post like toggle by its slug.
        return reverse('posts:post-like-api-toggle', kwargs={'post_slug': self.slug})    

    def get_image_url(self):
        """
        Retrun image url of the post if it has any.
        """
        if self.image and hasattr(self.image, 'url'):
            return self.image.url  

    def parent_comments(self):
        # Return all parent comments of an item.
        return Comment.objects.filter_by_parent(self) 


class CommentLike(PostAbstractRelationship):
    """
    A relationship model between the comment and its likes.
    """
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)


class CommentManager(models.Manager):
    """
    Override the comment manager.
    """
    def filter_by_parent(self, post):
        """
        Filter the comment queryset by parent comments.
        """
        qs = self.get_queryset().filter(post=post, reply=None)
        return qs


class Comment(models.Model):
    """
    Post comment model.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') # post.comments.all  comment.post.id
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True, through=CommentLike)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = CommentManager() 

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['created_at']

    def __str__(self):
        # Return comment post and user's full name.
        return f"{self.post} | {str(self.user.full_name)}"

    def get_update_absolute_url(self):
        # Return absolute url of update comment by its id.
        return reverse('posts:update-comment', kwargs={'comment_id': self.pk}) 

    def get_delete_absolute_url(self):
        # Return absolute url of delete comment by its id.
        return reverse('posts:delete-comment', kwargs={'comment_id': self.pk})

    def get_comment_likes_absolute_url(self):
        # Return absolute url of comment's likes by its id.
        return reverse('posts:comment-likes', kwargs={'comment_id': self.pk})             

    def get_api_like_url(self):
        # Return api url of the comment like toggle by its id.
        return reverse('posts:comment-like-api-toggle', kwargs={'comment_id': self.pk})      