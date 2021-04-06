from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from student.models import Student
from feedback.models import FeedbackStudent 
from adminhod.utils import paginate
from .utils import filter_students_feedbacks

def add_feedback_student(request):
    """
    Add student feedback.
    """
    # get current student.
    student = get_object_or_404(Student, user__id=request.user.id)
    # check if the request method is post.
    if request.method == "POST":
        # fetch submitted data.
        content = request.POST.get('feedback_message')
        # create new student feedback.
        FeedbackStudent.objects.create(student=student, content=content, reply="", is_replied=False)
        # display success message.
        messages.success(request, f'Your feedback has been added successfully.', extra_tags='add-feedback-student')
        # if save and add another.
        if 'save_and_add_another' in request.POST:
            # redirect to add student feedback url.
            return redirect('feedback-student:add-feedback')
        # if save.
        elif 'save' in request.POST:
            # redirect to view student feedbacks url.
            return redirect('feedback-student:view-feedback')
    return render(request, 'student/add_feedback_student.html', {})

def view_feedback_student(request):
    """
    Display all feedbacks of current student.
    Search current student's feedbacks by Date.  
    """
    # get all feedbacks of current student.
    feedbacks_qs = FeedbackStudent.objects.filter(student__user__id=request.user.id)
    # paginate the feedbacks list.
    page_obj_feedbacks = paginate(feedbacks_qs)
    if request.is_ajax():
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        data = dict()
        # filter current student's feedbacks by Date.
        feedbacks = feedbacks_qs.filter(created_at__contains=q)
        # paginate the feedbacks list.
        page_obj_feedbacks = paginate(feedbacks)
        context = {'feedbacks':page_obj_feedbacks, 'request':request}
        data['html_student_feedback_list'] = render_to_string('student/includes/partial_feedback_student_list.html', context)
        data['html_student_feedback_pagination'] = render_to_string('adminhod/includes/partial_feedback_adminhod_pagination.html', context)
        return JsonResponse(data)  
    context = {'feedbacks':page_obj_feedbacks}
    return render(request, 'student/view_feedback_student.html', context)

def paginate_feedback_student(request):
    """
    Paginate all feedbacks of current student.
    """
    # get all feedbacks of current student.
    feedbacks_qs = FeedbackStudent.objects.filter(student__user__id=request.user.id)
    # get page number of paginator.
    page_number = request.GET.get('page').split('&')[0]
    # get is replied value.
    is_replied = request.GET.get('is_replied')
    data = dict()
    # paginate the search results.
    if request.GET.get('search'):
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        # filter current student's feedbacks by Date.
        feedbacks = feedbacks_qs.filter(created_at__contains=q)
        # paginate the feedbacks list.
        page_obj_feedbacks = paginate(feedbacks, page_number)
    # paginate the filter results.
    elif is_replied:
        feedbacks = filter_students_feedbacks(
            is_replied=is_replied, 
            request=request,  
        )    
        # paginate the feedbacks list.
        page_obj_feedbacks = paginate(feedbacks, page_number)    
    else:
        # paginate the feedbacks list.
        page_obj_feedbacks = paginate(feedbacks_qs, page_number)    
    context = {'feedbacks':page_obj_feedbacks, 'request':request}
    data['html_student_feedback_list'] = render_to_string('student/includes/partial_feedback_student_list.html', context)
    data['html_student_feedback_pagination'] = render_to_string('adminhod/includes/partial_feedback_adminhod_pagination.html', context)
    return JsonResponse(data)

def feedback_detail_student(request, feedback_id):
    """
    Take student feedback's id, and view its details.
    """
    # get student feedback by its id.
    feedback = get_object_or_404(FeedbackStudent, pk=feedback_id)
    data = dict()
    context = {'feedback': feedback}
    data['html_form'] = render_to_string('student/feedback_detail_student.html', context, request=request)
    return JsonResponse(data)

@csrf_exempt
def filter_feedback_student(request):
    """
    Filter current student's feedbacks by Reply.
    """
    # get is replied value.
    is_replied = request.POST.get('is_replied')       
    data = dict()
    # filter staffs' feedbacks by Reply.
    feedbacks_qs = filter_students_feedbacks(
            is_replied=is_replied, 
            request=request,  
        )    
    if feedbacks_qs:
        # paginate the feedbacks list.
        page_obj_feedbacks = paginate(feedbacks_qs)
        context = {'feedbacks':page_obj_feedbacks, 'request':request}
    else:
        context = {'feedbacks':feedbacks_qs, 'request':request} 
    data['html_student_feedback_list'] = render_to_string('student/includes/partial_feedback_student_list.html', context)
    data['html_student_feedback_pagination'] = render_to_string('adminhod/includes/partial_feedback_adminhod_pagination.html', context)
    return JsonResponse(data)   