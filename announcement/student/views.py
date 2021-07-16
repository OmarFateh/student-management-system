from django.shortcuts import render
from django.db.models import Q

from announcement.models import Announcement
from course.models import Subject

# View Announcements
def view_announcements_student(request):
    """
    Display all announcements of current student's course.
    """
    # get list of all staffs' ids of current student's course.
    staff_ids_list = Subject.objects.staff_ids(request.user, is_student=True)
    # display all announcements of current student's course.
    announcements = Announcement.objects.filter(
        Q(adminhod=request.user.student.course.adminhod)|
        Q(staff__user__id__in=staff_ids_list) 
    ).distinct()
    # update announcements from not seen to be seen. 
    Announcement.objects.announcements_updated(request.user, staff_ids_list, is_student=True)
    context = {'announcements':announcements}
    return render(request, 'student/view_announcements.html', context)