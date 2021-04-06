import json

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt 

from course.models import Subject
from assignment.models import Assignment, StudentAssignment
from student.models import SessionYear
from adminhod.utils import paginate
from assignment.adminhod.utils import search
from .forms import AddAssignmentform
from .utils import filter_staffs_assignments, filter_staffs_submitted_assignments

def add_assignment(request):
    """
    Add assignments.
    """
    # check if the request method is post.
    if request.method == "POST":
        assignment_form = AddAssignmentform(request.POST, request=request)
        if assignment_form.is_valid():
            # create new assignment.
            assignment_form.save()
            # display success message.
            messages.success(request, f'New assignment has been added successfully.', extra_tags='add-assignment')
            # if save and add another.
            if 'save_and_add_another' in request.POST:
                # redirect to add assignment url.
                return redirect('assignment-staff:add-assignment')
            # if save.
            elif 'save' in request.POST:
                # redirect to manage assignments url.
                return redirect('assignment-staff:manage-assignment')
    else:
        assignment_form = AddAssignmentform(request=request)        
    context = {'form':assignment_form}        
    return render(request, 'staff/add_assignment.html', context)

def manage_assignment(request):
    """
    Display all assignment of current staff.
    Search assignments of current staff by deadline date.
    """
    # get all subjects of current staff.
    subjects = Subject.objects.filter(staff__user__id=request.user.id)
    # get all courses of current staff.
    courses = []
    for subject in subjects:
        if subject.course not in courses:
            courses.append(subject.course)
    # get all subjects ids of current staff.
    subjects_ids = subjects.values_list('id', flat=True)
    # get all assignments of current staff.
    assignments_qs = Assignment.objects.filter(subject__id__in=subjects_ids)
    # get all session years.
    session_years = SessionYear.objects.all()
    # paginate the assignments list.
    page_obj_assignments = paginate(assignments_qs)
    if request.is_ajax():
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        data = dict()
        # filter all assignments of current staff by deadline date.
        assignments = assignments_qs.filter(deadline_date__icontains=q)
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments)
        context = {'assignments':page_obj_assignments, 'request':request}
        data['html_assignment_list'] = render_to_string('staff/includes/partial_assignment_list.html', context)
        data['html_assignment_pagination'] = render_to_string('adminhod/includes/partial_assignment_pagination.html', context)
        return JsonResponse(data)  
    context = {'subjects':subjects, 'courses':courses, 'assignments':page_obj_assignments, 'session_years':session_years}
    return render(request, 'staff/manage_assignment.html', context)   

def get_subjects(request):
    """
    Get all subjects of a selected course.
    """
    # get course id.
    course_id = request.GET.get('course')
    # check if staff assignment or not.
    is_staff_assignment = request.GET.get('is_staff_assignment')
    # get list of subjects data of current course.
    if course_id and is_staff_assignment:
        subjects_list_data = Subject.objects.get_subjects_list_data(course_id, is_staff_assignment=True, user=request.user)
    elif course_id:
        subjects_list_data = Subject.objects.get_subjects_list_data(course_id)
    else:
        subjects_list_data = Subject.objects.get_subjects_list_data()    
    return JsonResponse(json.dumps(subjects_list_data), content_type='application/json', safe=False) 

@csrf_exempt
def filter_assignments(request):
    """
    Filter assignments of current staff by Course or Subject.
    """
    # get course id.
    course_id = request.POST.get('course_id')
    # get subject id.
    subject_id = request.POST.get('subject_id')
    # get session year id.
    session_year_id = request.POST.get('session_year_id')
    # get list of all subjects ids of current staff.
    subjects_ids = Subject.objects.filter(staff__user__id=request.user.id).values_list('id', flat=True)
    # get list of assignment data.
    data = dict()
    # filter assignments of current staff by Course, Subject or Session.
    assignments_qs = filter_staffs_assignments(
        course_id=course_id, 
        subject_id=subject_id, 
        session_year_id=session_year_id,
        subjects_ids=subjects_ids
    )    
    if assignments_qs:
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments_qs)
        context = {'assignments':page_obj_assignments, 'request':request}
    else:
        context = {'assignments':assignments_qs, 'request':request}
    data['html_assignment_list'] = render_to_string('staff/includes/partial_assignment_list.html', context)
    data['html_assignment_pagination'] = render_to_string('adminhod/includes/partial_assignment_pagination.html', context)
    return JsonResponse(data) 

def paginate_assignments(request):
    """
    Paginate all assignments of current staff. 
    """
    # get list all subjects ids of current staff.
    subjects_ids = Subject.objects.filter(staff__user__id=request.user.id).values_list('id', flat=True)
    # get all assignments of current staff.
    assignments_qs = Assignment.objects.filter(subject__id__in=subjects_ids)
    # get page number of paginator.
    page_number = request.GET.get('page').split('&')[0]
    # get course id.
    course_id = request.GET.get('course_id')
    # get subject id.
    subject_id = request.GET.get('subject_id')
    # get session year id.
    session_year_id = request.GET.get('session_year_id')
    # get list of submitted data.
    list_data = [course_id, subject_id, session_year_id]
    data = dict()
    # paginate the search results.
    if request.GET.get('search'):
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        # filter all assignments of current staff by deadline date.
        assignments = assignments_qs.filter(deadline_date__icontains=q)
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments, page_number)
    # paginate the filter results.
    elif any(list_data):
        assignments = filter_staffs_assignments(
            course_id=course_id, 
            subject_id=subject_id, 
            session_year_id=session_year_id,
            subjects_ids=subjects_ids
        )    
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments, page_number)    
    else:
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments_qs, page_number)    
    context = {'assignments':page_obj_assignments, 'request':request}
    data['html_assignment_list'] = render_to_string('staff/includes/partial_assignment_list.html', context)
    data['html_assignment_pagination'] = render_to_string('adminhod/includes/partial_assignment_pagination.html', context)
    return JsonResponse(data)

def update_assignment(request, assignment_id):
    """
    Take assignment's id, and get assignment by its id. 
    Update this assignment.
    """
    # get assignment by its id.
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    data = dict()
    # check if the request method is post.
    if request.method == 'POST':
        assignment_form = AddAssignmentform(request.POST, request=request, instance=assignment)
        if assignment_form.is_valid():
            # update assignment.
            assignment_form.save()
            data['form_is_valid'] = True 
            data['is_update'] = True
            # get list of all subjects ids of current staff.
            subjects_ids = Subject.objects.filter(staff__user__id=request.user.id).values_list('id', flat=True)
            # get all assignments of current staff.
            assignments = Assignment.objects.filter(subject__id__in=subjects_ids)
            data['html_assignment_list'] = render_to_string('staff/includes/partial_assignment_list.html', {'assignments': assignments})
        else:
            data['form_is_valid'] = False   
    else:
        assignment_form = AddAssignmentform(request=request, instance=assignment)
        context = {'form': assignment_form}
        data['html_form'] = render_to_string('staff/includes/partial_assignment_update.html', context, request=request)
    return JsonResponse(data)     

def delete_assignment(request, assignment_id):
    """
    Take assignment's id, and get assignment by its id. 
    Delete this assignment.
    """
    # get assignment by its id.
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    data = dict()
    # check if the request method is post.
    if request.method == 'POST':
        # delete assignment.
        assignment.delete()
        data['form_is_valid'] = True 
        data['is_update'] = False 
        # get list of all subjects ids of current staff.
        subjects_ids = Subject.objects.filter(staff__user__id=request.user.id).values_list('id', flat=True)
        # get all assignments of current staff.
        assignments = Assignment.objects.filter(subject__id__in=subjects_ids)
        data['html_assignment_list'] = render_to_string('staff/includes/partial_assignment_list.html', {'assignments': assignments})
    else:
        context = {'assignment': assignment}
        data['html_form'] = render_to_string('staff/includes/partial_assignment_delete.html', context, request=request)
    return JsonResponse(data) 

def view_submitted_assignments(request, assignment_slug):
    """
    Take assignment's slug, and get assignment by its slug.
    Display submitted assignments of this assignment.
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
        data['html_assignment_list'] = render_to_string('staff/includes/partial_submitted_assignments_list.html', context)
        data['html_assignment_pagination'] = render_to_string('adminhod/includes/partial_assignment_pagination.html', context)
        return JsonResponse(data)  
    context = {'assignments':page_obj_assignments, 'assignment':assignment}
    return render(request, 'staff/view_submitted_assignments.html', context)

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
        assignments = filter_staffs_submitted_assignments(
            submitted=submitted, 
            assignment=assignment, 
        )    
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments, page_number)    
    else:
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments_qs, page_number)    
    context = {'assignments':page_obj_assignments, 'request':request}
    data['html_assignment_list'] = render_to_string('staff/includes/partial_submitted_assignments_list.html', context)
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
    assignments_qs = filter_staffs_submitted_assignments(
        submitted=submitted, 
        assignment=assignment, 
    )    
    if assignments_qs:
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments_qs)
        context = {'assignments':page_obj_assignments, 'request':request}
    else:
        context = {'assignments':assignments_qs, 'request':request}
    data['html_assignment_list'] = render_to_string('staff/includes/partial_submitted_assignments_list.html', context)
    data['html_assignment_pagination'] = render_to_string('adminhod/includes/partial_assignment_pagination.html', context)
    return JsonResponse(data)