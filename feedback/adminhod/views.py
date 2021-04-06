from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt 

from feedback.models import FeedbackStaff, FeedbackStudent 
from student.models import SessionYear 
from course.models import Course, Subject
from adminhod.utils import paginate
from feedback.adminhod.utils import search, filter_adminhod_staffs_feedbacks, filter_adminhod_students_feedbacks

def view_feedback_staff_adminhod(request):
    """
    Display all staff feedbacks of current adminhod's courses.
    Search staffs' feedbacks by staffs' names.
    """
    # get list of all staffs' ids of current adminhod's courses.
    staffs_ids_list = Subject.objects.staff_ids(request.user)
    # get all staffs' feedbacks of current adminhod courses.
    feedbacks_qs = FeedbackStaff.objects.filter(staff__user__id__in=staffs_ids_list)
    # update staff feedbacks from not seen to be seen. 
    FeedbackStaff.objects.feedback_staff_updated(feedbacks_qs, request.user)
    # paginate the feedbacks list.
    page_obj_feedbacks = paginate(feedbacks_qs)
    if request.is_ajax():
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        data = dict()
        # filter staffs' feedbacks by staffs' names.
        feedbacks = search(q, staff_feedbacks_qs=feedbacks_qs, staffs_ids_list=staffs_ids_list)
        # paginate the feedbacks list.
        page_obj_feedbacks = paginate(feedbacks)
        context = {'feedbacks':page_obj_feedbacks, 'request':request}
        data['html_staff_feedback_list'] = render_to_string('adminhod/includes/partial_feedback_staff_adminhod_list.html', context)
        data['html_staff_feedback_pagination'] = render_to_string('adminhod/includes/partial_feedback_adminhod_pagination.html', context)
        return JsonResponse(data)  
    context = {'feedbacks':page_obj_feedbacks}
    return render(request, 'adminhod/view_feedback_staff_adminhod.html', context)

def view_feedback_student_adminhod(request):
    """
    Display all students feedbacks of current adminhod's courses.
    Search students' feedbacks by students' names. 
    """
    # get all courses of current adminhod.
    courses = Course.objects.filter(adminhod__user__id=request.user.id)
    # get list of courses' ids of current adminhod.
    courses_ids_list = courses.values_list('id', flat=True)
    # get all students feedbacks of current adminhod.
    feedbacks_qs = FeedbackStudent.objects.filter(student__course__id__in=courses_ids_list)
    # get all sessions.
    session_years = SessionYear.objects.all()
    # update students feedbacks from not seen to be seen. 
    FeedbackStudent.objects.feedback_student_updated(request.user)
    # paginate the feedbacks list.
    page_obj_feedbacks = paginate(feedbacks_qs)
    if request.is_ajax():
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        data = dict()
        # filter staffs' feedbacks by students' names.
        feedbacks = search(q, student_feedbacks_qs=feedbacks_qs, courses_ids_list=courses_ids_list)
        # paginate the feedbacks list.
        page_obj_feedbacks = paginate(feedbacks)
        context = {'feedbacks':page_obj_feedbacks, 'request':request}
        data['html_student_feedback_list'] = render_to_string('adminhod/includes/partial_feedback_student_adminhod_list.html', context)
        data['html_student_feedback_pagination'] = render_to_string('adminhod/includes/partial_feedback_adminhod_pagination.html', context)
        return JsonResponse(data)  
    context = {'feedbacks':page_obj_feedbacks, 'courses':courses, 'session_years':session_years}
    return render(request, 'adminhod/view_feedback_student_adminhod.html', context)

def paginate_staff_feedbacks(request):
    """
    Paginate all staff feedbacks of current adminhod's courses.
    """
    # get list of all staffs' ids of current adminhod's courses.
    staffs_ids_list = Subject.objects.staff_ids(request.user)
    # get all staffs' feedbacks of current adminhod courses.
    feedbacks_qs = FeedbackStaff.objects.filter(staff__user__id__in=staffs_ids_list)
    # get page number of paginator.
    page_number = request.GET.get('page').split('&')[0]
    # get is replied value.
    is_replied = request.GET.get('is_replied')
    data = dict()
    # paginate the search results.
    if request.GET.get('search'):
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        # filter staffs' feedbacks by staffs' names.        
        feedbacks = search(q, staff_feedbacks_qs=feedbacks_qs, staffs_ids_list=staffs_ids_list)
        # paginate the feedbacks list.
        page_obj_feedbacks = paginate(feedbacks, page_number)
    # paginate the filter results.
    elif is_replied:
        feedbacks = filter_adminhod_staffs_feedbacks(
            is_replied=is_replied, 
            staffs_ids_list=staffs_ids_list,  
        )    
        # paginate the feedbacks list.
        page_obj_feedbacks = paginate(feedbacks, page_number)     
    else:
        # paginate the feedbacks list.
        page_obj_feedbacks = paginate(feedbacks_qs, page_number)    
    context = {'feedbacks':page_obj_feedbacks, 'request':request}
    data['html_staff_feedback_list'] = render_to_string('adminhod/includes/partial_feedback_staff_adminhod_list.html', context)
    data['html_staff_feedback_pagination'] = render_to_string('adminhod/includes/partial_feedback_adminhod_pagination.html', context)
    return JsonResponse(data)

def paginate_student_feedbacks(request):
    """
    Paginate all udent feedbacks of current adminhod's courses.
    """
    # get list of courses' ids of current adminhod.
    courses_ids_list = Course.objects.filter(adminhod__user__id=request.user.id).values_list('id', flat=True)
    # get all students feedbacks of current adminhod.
    feedbacks_qs = FeedbackStudent.objects.filter(student__course__id__in=courses_ids_list)
    # get page number of paginator.
    page_number = request.GET.get('page').split('&')[0]
    # get course id.
    course_id = request.GET.get('course_id')
    # get session year id.
    session_year_id = request.GET.get('session_year_id')
    # get is replied value.
    is_replied = request.GET.get('is_replied')
    # get list of submitted data.
    list_data = [course_id, session_year_id, is_replied]
    data = dict()
    # paginate the search results.
    if request.GET.get('search'):
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        # filter staffs' feedbacks by students' names.
        feedbacks = search(q, student_feedbacks_qs=feedbacks_qs, courses_ids_list=courses_ids_list)
        # paginate the feedbacks list.
        page_obj_feedbacks = paginate(feedbacks, page_number)
    # paginate the filter results.
    elif any(list_data):
        feedbacks = filter_adminhod_students_feedbacks(
            is_replied=is_replied, 
            course_id=course_id,
            session_year_id=session_year_id,
            courses_ids_list=courses_ids_list,  
        )    
        # paginate the feedbacks list.
        page_obj_feedbacks = paginate(feedbacks, page_number)
    else:
        # paginate the feedbacks list.
        page_obj_feedbacks = paginate(feedbacks_qs, page_number)    
    context = {'feedbacks':page_obj_feedbacks, 'request':request}
    data['html_student_feedback_list'] = render_to_string('adminhod/includes/partial_feedback_student_adminhod_list.html', context)
    data['html_student_feedback_pagination'] = render_to_string('adminhod/includes/partial_feedback_adminhod_pagination.html', context)
    return JsonResponse(data)

@csrf_exempt
def filter_student_feedbacks(request):
    """
    Filter students' feedbacks by Course, Session or Reply.
    """
    # get course id.
    course_id = request.POST.get('course_id')
    # get session year id.
    session_year_id = request.POST.get('session_year_id')
    # get is replied value.
    is_replied = request.POST.get('is_replied')
    # get list all courses' ids of current adminhod.
    courses_ids_list = Course.objects.filter(adminhod__user__id=request.user.id).values_list('id', flat=True)
    # get list of students' feedbacks data.
    data = dict()
    # filter students' feedbacks by Course, Session or Reply.
    feedbacks_qs = filter_adminhod_students_feedbacks(
            is_replied=is_replied, 
            course_id=course_id,
            session_year_id=session_year_id,
            courses_ids_list=courses_ids_list,  
        )    
    if feedbacks_qs:
        # paginate the feedbacks list.
        page_obj_feedbacks = paginate(feedbacks_qs)
        context = {'feedbacks':page_obj_feedbacks, 'request':request}
    else:
        context = {'feedbacks':feedbacks_qs, 'request':request}  
    data['html_student_feedback_list'] = render_to_string('adminhod/includes/partial_feedback_student_adminhod_list.html', context)
    data['html_student_feedback_pagination'] = render_to_string('adminhod/includes/partial_feedback_adminhod_pagination.html', context)
    return JsonResponse(data)

@csrf_exempt
def filter_staff_feedbacks(request):
    """
    Filter staffs' feedbacks by Reply.
    """
    # get is replied value.
    is_replied = request.POST.get('is_replied')
    # get list of all staffs' ids of current adminhod's courses.
    staffs_ids_list = Subject.objects.staff_ids(request.user)    
    data = dict()
    # filter staffs' feedbacks by Reply.
    feedbacks_qs = filter_adminhod_staffs_feedbacks(
            is_replied=is_replied, 
            staffs_ids_list=staffs_ids_list,  
        )    
    if feedbacks_qs:
        # paginate the feedbacks list.
        page_obj_feedbacks = paginate(feedbacks_qs)
        context = {'feedbacks':page_obj_feedbacks, 'request':request}
    else:
        context = {'feedbacks':feedbacks_qs, 'request':request}
    data['html_staff_feedback_list'] = render_to_string('adminhod/includes/partial_feedback_staff_adminhod_list.html', context)
    data['html_staff_feedback_pagination'] = render_to_string('adminhod/includes/partial_feedback_adminhod_pagination.html', context)
    return JsonResponse(data)

def reply_feedback_staff(request, feedback_id):
    """
    Take staff feedback's id, and get feedback by its id.
    Reply to this staff feedback.
    """
    # get staff feedback by its id.
    feedback = get_object_or_404(FeedbackStaff, pk=feedback_id)
    # get list of all staffs' ids of current adminhod's courses.
    staffs_ids_list = Subject.objects.staff_ids(request.user) 
    data = dict()
    if request.method == 'POST':
        # fetch submitted data, and reply to feedback.
        feedback.reply = request.POST.get("reply")
        feedback.is_replied = True
        feedback.save()
        data['form_is_valid'] = True
        # get all staffs feedbacks of current adminhod's courses.
        feedbacks = FeedbackStaff.objects.filter(staff__user__id__in=staffs_ids_list)
        data['html_staff_feedback_list'] = render_to_string('adminhod/includes/partial_feedback_staff_adminhod_list.html', {'feedbacks': feedbacks})
    else:
        data['form_is_valid'] = False
    context = {"feedback": feedback}
    data['html_form'] = render_to_string('adminhod/includes/partial_staff_feedback_reply.html', context, request=request)
    return JsonResponse(data)

def reply_feedback_student(request, feedback_id):
    """
    Take student feedback's id, and get feedback by its id.
    Reply to this student feedback.
    """
    # get student feedback by its id.
    feedback = get_object_or_404(FeedbackStudent, pk=feedback_id)
    # get list all courses' ids of current adminhod.
    courses_ids_list = Course.objects.filter(adminhod__user__id=request.user.id).values_list('id', flat=True)
    data = dict()
    if request.method == 'POST':
        # fetch submitted data, and reply to feedback.
        feedback.reply = request.POST.get("reply")
        feedback.is_replied = True
        feedback.save()
        data['form_is_valid'] = True
        # get all students feedbacks of current adminhod's courses.
        feedbacks = FeedbackStudent.objects.filter(student__course__id__in=courses_ids_list) 
        data['html_student_feedback_list'] = render_to_string('adminhod/includes/partial_feedback_student_adminhod_list.html', {'feedbacks': feedbacks})
    else:
        data['form_is_valid'] = False
    context = {"feedback": feedback}
    data['html_form'] = render_to_string('adminhod/includes/partial_student_feedback_reply.html', context, request=request)
    return JsonResponse(data)