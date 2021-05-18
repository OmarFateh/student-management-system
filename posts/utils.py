from django.core.paginator import Paginator


def paginate_posts(posts_qs, page_number=1):
    """
    Take a queryset of posts, and page number with a default value of 1, and paginate the queryset.
    """
    paginator_posts = Paginator(posts_qs, 10) # display 1 objects per page.
    return paginator_posts.get_page(page_number)