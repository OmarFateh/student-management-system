from django.contrib import admin

from .models import Post, PostLike, Comment #, PostFavourite


# class PostFavouriteAdmin(admin.TabularInline):
#     """
#     Display the post favourite model as a tabular inline.
#     """
#     model = PostFavourite


class PostLikeAdmin(admin.TabularInline):
    """
    Display the post like model as a tabular inline.
    """
    model = PostLike

class PostAdmin(admin.ModelAdmin):
    """
    Override the user profile admin and customize the posts display.
    """
    inlines       = [PostLikeAdmin] #,PostFavouriteAdmin
    # list_display  = []
    # search_fields = []

    class Meta:
        model = Post



# models admin site registeration 
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
