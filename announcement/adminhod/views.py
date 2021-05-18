from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string

from adminhod.models import AdminHOD
from announcement.models import Announcement
from course.models import Subject
from .forms import AddAnnouncementForm

# View Announcements
def view_announcements_adminhod(request):
    """
    Display all announcements for adminhod.
    """
    # get current adminhod.
    adminhod = get_object_or_404(AdminHOD, user__id=request.user.id)
    # get list of all staffs' ids of current adminhod's courses.
    staffs_ids_list = Subject.objects.staff_ids(request.user)
    # display all announcements.
    announcements = Announcement.objects.filter(
        Q(adminhod=adminhod)|
        Q(staff__user__id__in=staffs_ids_list) 
    ).distinct()
    # update from not seen to be seen. 
    Announcement.objects.announcements_updated(request.user, staffs_ids_list)
    context = {'announcements':announcements, 'adminhod':adminhod}
    return render(request, 'adminhod/view_announcements.html', context)

# Add Announcements
def add_announcement_form(request, form, template_name, adminhod=None, staff=None):
    """
    Take form, template name, and adminhod or staff.
    Add announcement for in case of taking adminhod. 
    Add announcement for in case of taking staff. 
    """
    # check if the request method is post.
    if request.method == "POST":
        # if the form is valid.
        if form.is_valid():
            # fetch submitted data and create new announcement.
            header = form.cleaned_data.get("header")
            content = form.cleaned_data.get("content")
            # check if this announcement is from adminhod.
            if adminhod:
                Announcement.objects.create(
                    header=header, 
                    content=content, 
                    adminhod=adminhod, 
                    is_adminhod=True,
                    is_staff=False,
                )
                # Display success message.
                messages.success(request, f'New Announcement has been added successfully.', extra_tags='add-announcements-adminhod')
                # if save and add another.
                if 'save_and_add_another' in request.POST:
                    # redirect to add announcements url.
                    return redirect('announcement-adminhod:add-announcements')
                # if save.
                elif 'save' in request.POST:
                    # redirect to view announcements url.
                    return redirect('announcement-adminhod:view-announcements')
            # check if this announcement is from staff.
            elif staff:
                Announcement.objects.create(
                    header=header, 
                    content=content, 
                    staff=staff, 
                    is_staff=True,
                    is_adminhod=False,
                )
                # Display success message.
                messages.success(request, f'New Announcement has been added successfully.', extra_tags='add-announcements-staff')
                # if save and add another.
                if 'save_and_add_another' in request.POST:
                    # redirect to add announcements url.
                    return redirect('announcement-staff:add-announcements')
                # if save.
                elif 'save' in request.POST:
                    # redirect to view announcements url.
                    return redirect('announcement-staff:view-announcements')

    context = {'form':form}
    return render(request, template_name, context) 

def add_announcement_adminhod(request):
    """
    Add announcements.
    """
    # get current adminhod.
    adminhod = get_object_or_404(AdminHOD, user__id=request.user.id)
    if request.method == 'POST':
        announcement_form = AddAnnouncementForm(request.POST)
    else:
        announcement_form = AddAnnouncementForm()
    return add_announcement_form(request, announcement_form, 'adminhod/add_announcements.html', adminhod)      

def delete_announcement_adminhod(request, announcement_id):
    """
    Take announcement's id, and get announcement by its id. 
    Delete this announcement. 
    """
    # get announcement by its id.
    announcement = get_object_or_404(Announcement, pk=announcement_id)
    # get current adminhod.
    adminhod = get_object_or_404(AdminHOD, user__id=request.user.id)
    data = dict()
    if announcement.adminhod == adminhod:
        if request.method == 'POST':
            # delete announcement.
            announcement.delete()
            data['form_is_valid'] = True 
            # get all announcements. 
            announcements = Announcement.objects.all()
            context = {'announcements': announcements, 'adminhod':adminhod}
            data['html_announcement_list'] = render_to_string('adminhod/includes/partial_announcement_list.html', context)
        else:
            context = {'announcement': announcement}
            data['html_form'] = render_to_string('adminhod/includes/partial_announcement_delete.html', context, request=request)
    return JsonResponse(data)    
