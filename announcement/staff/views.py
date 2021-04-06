from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string

from staff.models import Staff
from course.models import Subject
from announcement.models import Announcement
from announcement.adminhod.forms import AddAnnouncementForm
from announcement.adminhod.views import add_announcement_form

# View Announcements
def view_announcements_staff(request):
    """
    Display all announcements of current staff's courses.
    """
    # get list of all staffs' ids of current staff's courses.
    staff_ids_list = Subject.objects.staff_ids(request.user, is_staff=True)
    # get list of all adminhods' ids of current staff's courses
    adminhod_ids_list = Subject.objects.courses_adminhods_ids(request.user)
    # display all announcements of current staff's courses.
    announcements = Announcement.objects.filter(
        Q(adminhod__id__in=adminhod_ids_list)|
        Q(staff__id__in=staff_ids_list) 
    ).distinct()
    # get current staff.
    staff = get_object_or_404(Staff, user__id=request.user.id)
    # display all announcements.
    announcements = Announcement.objects.all()
    # update announcements from not seen to be seen. 
    Announcement.objects.announcements_updated(request.user, staff_ids_list, adminhod_ids_list, is_staff=True)
    context = {'announcements':announcements, 'staff':staff}
    return render(request, 'staff/view_announcements.html', context)
   
def add_announcement_staff(request):
    """
    Add announcements.
    """
    # get current staff.
    staff = get_object_or_404(Staff, user__id=request.user.id)
    if request.method == 'POST':
        announcement_form = AddAnnouncementForm(request.POST)
    else:
        announcement_form = AddAnnouncementForm()
    return add_announcement_form(request, announcement_form, 'staff/add_announcements.html', staff=staff)

def delete_announcement_staff(request, announcement_id):
    """
    Take announcement's id, and get announcement by its id. 
    Delete this announcement.
    """
    # get announcement by its id.
    announcement = get_object_or_404(Announcement, pk=announcement_id)
    # get current staff.
    staff = get_object_or_404(Staff, user__id=request.user.id)
    data = dict()
    if announcement.staff == staff:
        if request.method == 'POST':
            # delete announcement.
            announcement.delete()
            data['form_is_valid'] = True 
            # get all announcements. 
            announcements = Announcement.objects.all()
            context = {'announcements': announcements, 'staff':staff}
            data['html_announcement_list'] = render_to_string('staff/includes/partial_announcement_list.html', context)
        else:
            context = {'announcement': announcement}
            data['html_form'] = render_to_string('staff/includes/partial_announcement_delete.html', context, request=request)
    return JsonResponse(data)    