from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt 

from course.models import Subject
from student.models import Student
from assignment.models import Assignment
from adminhod.utils import paginate
from .forms import UploadAssignmentform
from .utils import filter_students_assignments

def view_assignments(request):
    """
    Display all assignments of current student, and update them from not seen to be seen.
    Search assignments of current student by deadline date.
    """
    # get all subjects of current student.
    subjects = Subject.objects.filter(course__student__user__id=request.user.id)
    # get all subjects ids of current student.
    subjects_ids = Subject.objects.student_subjects_ids(request.user)
    # get all assignments of current student.
    assignments_qs = Assignment.objects.student_assignments(subjects_ids, request.user)
    # update from not seen to be seen. 
    Assignment.objects.assignments_updated(request.user.student)
    # paginate the assignments list.
    page_obj_assignments = paginate(assignments_qs)
    if request.is_ajax():
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        data = dict()
        # filter all assignments of current student.
        assignments = assignments_qs.filter(deadline_date__icontains=q)
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments)
        context = {'assignments':page_obj_assignments, 'request':request}
        data['html_assignment_list'] = render_to_string('student/includes/partial_assignment_list.html', context)
        data['html_assignment_pagination'] = render_to_string('adminhod/includes/partial_assignment_pagination.html', context)
        return JsonResponse(data)  
    context = {'assignments':page_obj_assignments, 'subjects':subjects}
    return render(request, 'student/view_assignment.html', context)

def assignment_detail(request, assignment_id):
    """
    Take assignment's id, and display its details.
    """
    # get assignment by its id.
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    data = dict()
    context = {'assignment': assignment}
    data['html_form'] = render_to_string('student/includes/partial_assignment_detail.html', context, request=request)
    return JsonResponse(data)     

def upload_assignment(request, assignment_id):
    """
    Take assignment's id, and get assignment by its id. 
    Upload document for this assignment.
    """
    # get assignment by its id.
    assignment_obj = get_object_or_404(Assignment, pk=assignment_id)
    # get current student.
    student = get_object_or_404(Student, user__id=request.user.id)
    data = dict()
     # check if the request method is post.
    if request.method == 'POST':
        assignment_form = UploadAssignmentform(request.POST, request.FILES)
        if assignment_form.is_valid():
            # upload assignment.
            form = assignment_form.save(commit=False)
            form.student = student
            form.assignment = assignment_obj
            form.save()
            # add current student to list of students who submitted this assignment.
            assignment_obj.is_submitted.add(student)
            assignment_obj.save()
            data['form_is_valid'] = True 
            # get all subjects ids of current student.
            subjects_ids = Subject.objects.student_subjects_ids(request.user)
            # get all assignments of current student.
            assignments = Assignment.objects.student_assignments(subjects_ids, request.user)
            data['html_assignment_list'] = render_to_string('student/includes/partial_assignment_list.html', {'assignments': assignments, 'user':request.user})
        else:
            data['form_is_valid'] = False   
    else:
        assignment_form = UploadAssignmentform()
        context = {'assignment': assignment_obj, 'form':assignment_form}
        data['html_form'] = render_to_string('student/includes/partial_assignment_upload.html', context, request=request)
    return JsonResponse(data)     

@csrf_exempt
def filter_student_assignments(request):
    """
    Filter assignments of current student by Subject or whether it's been submitted or not.
    """
    # get subject id.
    subject_id = request.POST.get('subject_id')
    # get is submitted value.
    is_submitted = request.POST.get('is_submitted') 
    # get list of assignment data.
    data = dict()
    # filter assignments of current student by Subject or whether it's been submitted or not.
    assignments_qs = filter_students_assignments(
        subject_id=subject_id, 
        is_submitted=is_submitted, 
        request=request
    )    
    if assignments_qs:
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments_qs)
        context = {'assignments':page_obj_assignments, 'request':request}
    else:
        context = {'assignments':assignments_qs, 'request':request}
    data['html_assignment_list'] = render_to_string('student/includes/partial_assignment_list.html', context)
    data['html_assignment_pagination'] = render_to_string('adminhod/includes/partial_assignment_pagination.html', context)
    return JsonResponse(data)         

def paginate_student_assignments(request):
    """
    Paginate all assignments of current student.
    """
    # get all subjects ids of current student.
    subjects_ids = Subject.objects.student_subjects_ids(request.user)
    # get all assignments of current student.
    assignments_qs = Assignment.objects.student_assignments(subjects_ids, request.user)
    # get page number of paginator.
    page_number = request.GET.get('page').split('&')[0]
    # get subject id.
    subject_id = request.GET.get('subject_id')
    # get is submitted value.
    is_submitted = request.GET.get('is_submitted')
    # get list of submitted data.
    list_data = [subject_id, is_submitted] 
    data = dict()
    # paginate the search results.
    if request.GET.get('search'):
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        # filter all assignments of current student by deadline date.
        assignments = assignments_qs.filter(deadline_date__icontains=q)
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments, page_number)
    # paginate the filter results.
    elif any(list_data):
        assignments = filter_students_assignments(
            subject_id=subject_id, 
            is_submitted=is_submitted, 
            request=request
        )    
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments, page_number)    
    else:
        # paginate the assignments list.
        page_obj_assignments = paginate(assignments_qs, page_number)    
    context = {'assignments':page_obj_assignments, 'request':request}
    data['html_assignment_list'] = render_to_string('student/includes/partial_assignment_list.html', context)
    data['html_assignment_pagination'] = render_to_string('adminhod/includes/partial_assignment_pagination.html', context)
    return JsonResponse(data)