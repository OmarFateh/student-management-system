from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from staff.models import Staff
from feedback.models import FeedbackStaff 
from adminhod.utils import paginate
from .utils import filter_staffs_feedbacks


def add_feedback_staff(request):
    """
    Add staff feedback.
    """
    # get current staff.
    staff = get_object_or_404(Staff, user__id=request.user.id)
    # check if the request method is post.
    if request.method == "POST":
        # fetch submitted data.
        content = request.POST.get('feedback_message')
        # create new staff feedback.
        FeedbackStaff.objects.create(staff=staff, content=content, reply="", is_replied=False)
        # display success message.
        messages.success(request, f'Your feedback has been added successfully.', extra_tags='add-feedback-staff')
        # if save and add another.
        if 'save_and_add_another' in request.POST:
            # redirect to add staff feedback url. 
            return redirect('feedback-staff:add-feedback')
        # if save.
        elif 'save' in request.POST:
            # redirect to view staff feedbacks url.
            return redirect('feedback-staff:view-feedback')
    return render(request, 'staff/add_feedback_staff.html', {})

def view_feedback_staff(request):
    """
    Display all feedbacks of current staff.
    Search current staff's feedbacks by Date.  
    """
    # get all feedbacks of current staff.
    feedbacks_qs = FeedbackStaff.objects.filter(staff__user__id=request.user.id)
    # paginate the feedbacks list.
    page_obj_feedbacks = paginate(feedbacks_qs)
    if request.is_ajax():
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        data = dict()
        # filter current staff's feedbacks by Date.
        feedbacks = feedbacks_qs.filter(created_at__contains=q)
        # paginate the feedbacks list.
        page_obj_feedbacks = paginate(feedbacks)
        context = {'feedbacks':page_obj_feedbacks, 'request':request}
        data['html_staff_feedback_list'] = render_to_string('staff/includes/partial_feedback_staff_list.html', context)
        data['html_staff_feedback_pagination'] = render_to_string('adminhod/includes/partial_feedback_adminhod_pagination.html', context)
        return JsonResponse(data)  
    context = {'feedbacks':page_obj_feedbacks}
    return render(request, 'staff/view_feedback_staff.html', context)

def paginate_feedback_staff(request):
    """
    Paginate all feedbacks of current staff.
    """
    # get all feedbacks of current staff.
    feedbacks_qs = FeedbackStaff.objects.filter(staff__user__id=request.user.id)
    # get page number of paginator.
    page_number = request.GET.get('page').split('&')[0]
    # get is replied value.
    is_replied = request.GET.get('is_replied')
    data = dict()
    # paginate the search results.
    if request.GET.get('search'):
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        # filter current staff's feedbacks by Date.
        feedbacks = feedbacks_qs.filter(created_at__contains=q)
        # paginate the feedbacks list.
        page_obj_feedbacks = paginate(feedbacks, page_number)
    # paginate the filter results.
    elif is_replied:
        feedbacks = filter_staffs_feedbacks(
            is_replied=is_replied, 
            request=request,  
        )    
        # paginate the feedbacks list.
        page_obj_feedbacks = paginate(feedbacks, page_number)    
    else:
        # paginate the feedbacks list.
        page_obj_feedbacks = paginate(feedbacks_qs, page_number)    
    context = {'feedbacks':page_obj_feedbacks, 'request':request}
    data['html_staff_feedback_list'] = render_to_string('staff/includes/partial_feedback_staff_list.html', context)
    data['html_staff_feedback_pagination'] = render_to_string('adminhod/includes/partial_feedback_adminhod_pagination.html', context)
    return JsonResponse(data)

def feedback_detail_staff(request, feedback_id):
    """
    Take staff feedback's id, and view its details.
    """
    # get staff feedback by its id.
    feedback = get_object_or_404(FeedbackStaff, pk=feedback_id)
    data = dict()
    context = {'feedback': feedback}
    data['html_form'] = render_to_string('staff/feedback_detail_staff.html', context, request=request)
    return JsonResponse(data)

@csrf_exempt
def filter_feedback_staff(request):
    """
    Filter current staff's feedbacks by Reply.
    """
    # get is replied value.
    is_replied = request.POST.get('is_replied')    
    data = dict()
    # filter staffs' feedbacks by Reply.
    feedbacks_qs = filter_staffs_feedbacks(
            is_replied=is_replied, 
            request=request,  
        )    
    if feedbacks_qs:
        # paginate the feedbacks list.
        page_obj_feedbacks = paginate(feedbacks_qs)
        context = {'feedbacks':page_obj_feedbacks, 'request':request}
    else:
        context = {'feedbacks':feedbacks_qs, 'request':request}   
    data['html_staff_feedback_list'] = render_to_string('staff/includes/partial_feedback_staff_list.html', context)
    data['html_staff_feedback_pagination'] = render_to_string('adminhod/includes/partial_feedback_adminhod_pagination.html', context)
    return JsonResponse(data)