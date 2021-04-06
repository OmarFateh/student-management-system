import random
import string

from django.db.models import Q
from django.core.paginator import Paginator

def random_string_generator(length=10):
    """
    Generate a random alphanumeric string of letters and digits of a given fixed length.
    """
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

def unique_slug_generator(instance, new_slug=None):
    """
    Generate a unique slug of given instance.
    """
    # check if the given arguments have a value of new slug
    # if yes, assign the given value to the slug field. 
    if new_slug is not None:
        slug = new_slug
    # if not, generate a slug of a random string.
    else:
        slug = random_string_generator()
    # get the instance class. 
    Klass = instance.__class__
    # check if there's any item with the same slug.
    qs_exists = Klass.objects.filter(slug=slug).exists()
    # if yes, generate a new slug of a random string and return recursive function with the new slug.
    if qs_exists:
        new_slug = random_string_generator()
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

def filter_list(filter_qs_list):
    """
    Take a list of querysets, and return the intersection.
    """
    # check if the list has a non string object type.
    if any([type(x) != str for x in filter_qs_list if x]):    
        # get a list of all non null objects.
        filter_qs = [i for i in filter_qs_list if i]
        if filter_qs:
            # get intersection between querysets.        
            merged_qs = list(set(filter_qs[0]).intersection(*filter_qs))
            qs = merged_qs
        else:
            qs = filter_qs     
    else:
        qs = None 
    return qs

def search(q, staff_student_qs=None, session_qs=None):
    """
    Take search value, q.
    In case of taking a staff or student queryset, filter the queryset by name or email.
    In case of taking session queryset, filter the queryset by start or end date, ordered by start date.
    """
    if staff_student_qs:
        # filter staff or students by name or email, ordered alphabetically by user's full name.
        return staff_student_qs.filter(
                Q(user__full_name__startswith=q)|
                Q(user__email__startswith=q)
            ).distinct().order_by('user__full_name')
    elif session_qs:
        # filter sessions by start or end date, ordered by start date.
        return session_qs.filter(
            Q(start_date__icontains=q)|
            Q(end_date__icontains=q)
        ).distinct().order_by('start_date')           

def paginate(qs, page_number=1):
    """
    Take a queryset, and page number with a default value of 1, and paginate the queryset.
    """
    paginator_qs = Paginator(qs, 1) # display 10 objects per page.
    return paginator_qs.get_page(page_number)