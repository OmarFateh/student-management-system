from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt 

from course.models import Course, Subject
from student.models import SessionYear
from assignment.models import Assignment, StudentAssignment
from adminhod.utils import filter_list, paginate
from .utils import search, filter_adminhod_assignments, filter_adminhod_submitted_assignments

def view_assignments(request):
    """
    Display all assignments for adminhod, and update them from not seen to be seen.
    Search assignments by deadline date. 
    """
    # get all courses of current adminhod.
    courses = Course.objects.filter(adminhod__user__id=request.user.id)
    # get all subjects of current adminhod's courses.
    subjects = Subject.objects.filter(course__in=courses)
    # get all session years.
    session_years = SessionYear.objects.all()
    # get all assignments.
    assignments_qs = Assignment.objects.filter(subject__in=subjects)
    # update from not seen to be seen. 
    Assignment.objects.assignments_updated()
    # paginate the assignments list.
    page_obj_assignments = paginate(assignments_qs)
    if request.is_ajax():
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        data = dict()
        # filter all assignments of current adminhod.
        assignments = search(q, assignments_qs)
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments)
        context = {'assignments':page_obj_assignments, 'request':request}
        data['html_assignment_list'] = render_to_string('adminhod/includes/partial_assignment_list.html', context)
        data['html_assignment_pagination'] = render_to_string('adminhod/includes/partial_assignment_pagination.html', context)
        return JsonResponse(data)  
    context = {'assignments':page_obj_assignments, 'subjects':subjects, 'courses':courses, 'session_years':session_years}
    return render(request, 'adminhod/view_assignments.html', context)

def assignment_detail(request, assignment_id):
    """
    Take assignment's id, and display its details. 
    """
    # get assignment by its id.
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    data = dict()
    context = {'assignment': assignment}
    data['html_form'] = render_to_string('adminhod/includes/partial_assignment_detail.html', context, request=request)
    return JsonResponse(data) 

def paginate_assignments(request):
    """
    Paginate all assignments of current adminhod. 
    """
    # get list of all subjects' ids of current adminhod's courses.
    subjects_ids_list = Subject.objects.user_subjects(request.user, is_ids=True)
    # get all assignments of current adminhod courses.
    assignments_qs = Assignment.objects.filter(subject__id__in=subjects_ids_list)
    # get page number of paginator.
    page_number = request.GET.get('page').split('&')[0]
    # get course id.
    course_id = request.GET.get('course_id')
    # get session year id.
    session_year_id = request.GET.get('session_year_id')
    # get subject id.
    subject_id = request.GET.get('subject_id')
    # get list of submitted data.
    list_data = [course_id, session_year_id, subject_id]
    data = dict()
    # paginate the search results.
    if request.GET.get('search'):
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        # filter all assignments of current adminhod by deadline date.
        assignments = search(q, assignments_qs)
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments, page_number)
    # paginate the filter results.
    elif any(list_data):
        assignments = filter_adminhod_assignments(
            course_id=course_id, 
            subject_id=subject_id, 
            session_year_id=session_year_id,
            subjects_ids_list=subjects_ids_list
        )    
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments, page_number)        
    else:
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments_qs, page_number)    
    context = {'assignments':page_obj_assignments, 'request':request}
    data['html_assignment_list'] = render_to_string('adminhod/includes/partial_assignment_list.html', context)
    data['html_assignment_pagination'] = render_to_string('adminhod/includes/partial_assignment_pagination.html', context)
    return JsonResponse(data)    

@csrf_exempt
def filter_assignments(request):
    """
    Filter assignments by Course, Subject, or Session Year.
    """
    # get course id.
    course_id = request.POST.get('course_id')
    # get session year id.
    session_year_id = request.POST.get('session_year_id')
    # get subject id.
    subject_id = request.POST.get('subject_id')
    # get list of all subjects' ids of current adminhod's courses.
    subjects_ids_list = Subject.objects.user_subjects(request.user, is_ids=True)
    # get list of Assignment data.
    data = dict()
    # filter assignments by Course, Subject, or Session Year.
    assignments_qs = filter_adminhod_assignments(
        course_id=course_id, 
        subject_id=subject_id, 
        session_year_id=session_year_id,
        subjects_ids_list=subjects_ids_list
    )    
    if assignments_qs:
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments_qs)
        context = {'assignments':page_obj_assignments, 'request':request}
    else:
        context = {'assignments':assignments_qs, 'request':request}
    data['html_assignment_list'] = render_to_string('adminhod/includes/partial_assignment_list.html', context)
    data['html_assignment_pagination'] = render_to_string('adminhod/includes/partial_assignment_pagination.html', context)
    return JsonResponse(data)

def view_submitted_assignments(request, assignment_slug):
    """
    Take assignment's slug, and get assignment by its slug.
    Display submitted assignments of this assignment.
    Search submitted assignments of this assignment by student's name and submission date, 
    ordered alphabetically by student's name.
    """
    # get assignment by its slug.
    assignment = get_object_or_404(Assignment, slug=assignment_slug)
    # get all submitted assignments of this assignment.
    assignments_qs = StudentAssignment.objects.filter(assignment=assignment)
    # paginate the assignments list.
    page_obj_assignments = paginate(assignments_qs)
    if request.is_ajax():
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        data = dict()
        # filter submitted assignments of this assignment by student's name and submission date.
        assignments = search(q, assignments_qs)
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments)
        context = {'assignments':page_obj_assignments, 'request':request}
        data['html_assignment_list'] = render_to_string('adminhod/includes/partial_submitted_assignments_list.html', context)
        data['html_assignment_pagination'] = render_to_string('adminhod/includes/partial_assignment_pagination.html', context)
        return JsonResponse(data)  
    context = {'assignments':page_obj_assignments, 'assignment':assignment}
    return render(request, 'adminhod/view_submitted_assignments.html', context)

def paginate_submitted_assignments(request, assignment_slug):
    """
    Take assignment's slug, and get assignment by its slug.
    Paginate all submitted assignments of this assignment.
    """
    # get assignment by its slug.
    assignment = get_object_or_404(Assignment, slug=assignment_slug)
    # get all submitted assignments of this assignment.
    assignments_qs = StudentAssignment.objects.filter(assignment=assignment)
    # get page number of paginator.
    page_number = request.GET.get('page').split('&')[0]
    # get submitted data.
    submitted = request.GET.get('is_submitted')
    data = dict()
    # paginate the search results.
    if request.GET.get('search'):
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        # filter all submitted assignments of this assignment by student's name and submission date.
        assignments = search(q, assignments_qs)
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments, page_number)
    # paginate the filter results.
    elif submitted:
        assignments = filter_adminhod_submitted_assignments(
            submitted=submitted, 
            assignment=assignment, 
        )    
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments, page_number)    
    else:
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments_qs, page_number)    
    context = {'assignments':page_obj_assignments, 'request':request}
    data['html_assignment_list'] = render_to_string('adminhod/includes/partial_submitted_assignments_list.html', context)
    data['html_assignment_pagination'] = render_to_string('adminhod/includes/partial_assignment_pagination.html', context)
    return JsonResponse(data)    

@csrf_exempt
def filter_submitted_assignments(request, assignment_slug):
    """
    Take assignment's slug, and get assignment by its slug.
    Filter submitted assignments of this assignment by submission date, whether before or after the deadline date. 
    """
    # get assignment by its slug.
    assignment = get_object_or_404(Assignment, slug=assignment_slug)
    # get submitted data.
    submitted = request.POST.get('is_submitted')
    data = dict()
    # filter assignments of current staff by Course, Subject or Session.
    assignments_qs = filter_adminhod_submitted_assignments(
        submitted=submitted, 
        assignment=assignment, 
    )    
    if assignments_qs:
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments_qs)
        context = {'assignments':page_obj_assignments, 'request':request}
    else:
        context = {'assignments':assignments_qs, 'request':request}
    data['html_assignment_list'] = render_to_string('adminhod/includes/partial_submitted_assignments_list.html', context)
    data['html_assignment_pagination'] = render_to_string('adminhod/includes/partial_assignment_pagination.html', context)
    return JsonResponse(data)

