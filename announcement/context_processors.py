from announcement.models import Announcement
from course.models import Subject


def announcements_count(request):
    """
    Custom context processor for announcements count.
    """
    count_announcements = 0
    # check if current user is authenticated or not.
    if request.user.is_authenticated:
        if request.user.user_type == 'STUDENT':
            # get list of all staffs' ids of current student's course.
            staff_ids_list = Subject.objects.staff_ids(request.user, is_student=True)
            # get announcements count.
            count_announcements = Announcement.objects.announcements_count(request.user, staff_ids_list, is_student=True)
        elif request.user.user_type == 'STAFF':
            # get list of all staffs' ids of current staff's courses.
            staff_ids_list = Subject.objects.staff_ids(request.user, is_staff=True)
            # get list of all adminhods' ids of current staff's courses.
            adminhod_ids_list = Subject.objects.courses_adminhods_ids(request.user) 
            # get announcements count.
            count_announcements = Announcement.objects.announcements_count(request.user, staff_ids_list, adminhod_ids_list, is_staff=True)
        elif request.user.user_type == 'HOD':
            # get list of all staffs' ids of current adminhod's courses.
            staff_ids_list = Subject.objects.staff_ids(request.user) 
            # get announcements count.
            count_announcements = Announcement.objects.announcements_count(request.user, staff_ids_list)
    return {'count_announcements':count_announcements} 



           