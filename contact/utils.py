from django.db.models import Q
from django.core.paginator import Paginator

def search(q, staff_student_qs):
    """
    Take search value, q, and a staff or student queryset, and filter by name or email.
    """
    return staff_student_qs.filter(
            Q(user__full_name__startswith=q)|
            Q(user__email__startswith=q)
        ).distinct().order_by('user__full_name')

def paginate(staff_student_qs, page_number=1):
    """
    Take a staff or student queryset, and page number with a default value of 1, and paginate the queryset.
    """
    paginator_staffs_students = Paginator(staff_student_qs, 9) # display 1 objects per page.
    return paginator_staffs_students.get_page(page_number)