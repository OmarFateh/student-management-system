from django.contrib import admin

from .models import Post, PostLike, Comment, CommentLike


class PostLikeAdmin(admin.TabularInline):
    """
    Display the post like model as a tabular inline.
    """
    model = PostLike


class PostAdmin(admin.ModelAdmin):
    """
    Override the post admin and customize the posts display.
    """
    inlines = [PostLikeAdmin]

    class Meta:
        model = Post


class CommentLikeAdmin(admin.TabularInline):
    """
    Display the comment like model as a tabular inline.
    """
    model = CommentLike


class CommentAdmin(admin.ModelAdmin):
    """
    Override the comment admin and customize the comments display.
    """
    inlines = [CommentLikeAdmin]

    class Meta:
        model = Comment


# models admin site registeration 
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
