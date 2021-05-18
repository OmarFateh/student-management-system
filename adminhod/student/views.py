from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt 

from student.models import Student, SessionYear 
from course.models import Course
from adminhod.utils import search, paginate
from adminhod.staff.views import add_staff_student_form, update_staff_student_form
from .forms import AddStudentForm, UpdateStudentAdminForm
from .utils import filter_students


def add_student(request):
    """
    Add student.
    """
    user_type = 'STUDENT'
    if request.method == 'POST':
        student_form = AddStudentForm(request.POST, request.FILES, request=request)
    else:
        student_form = AddStudentForm(request=request)
    return add_staff_student_form(request, student_form, 'student/add_student.html', user_type)

def manage_student(request):
    """
    Display all students of current adminhod's courses.
    Search students of current adminhod by name or email, ordered alphabetically by name.
    """
    # get all courses of current adminhod.
    courses = Course.objects.filter(adminhod__user__id=request.user.id)
    # get all students of current adminhod's courses. 
    students_qs = Student.objects.filter(course__in=courses).order_by('course')
    # get all sessions.
    session_years = SessionYear.objects.all()
    # paginate the students list.
    page_obj_students = paginate(students_qs)
    if request.is_ajax():
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        data = dict()  
        # filter students by name or email, ordered alphabetically by name.
        students = search(q, students_qs)
        # paginate the students list.
        page_obj_students = paginate(students)    
        context = {'students': page_obj_students, 'request':request}
        data['html_student_list'] = render_to_string('student/includes/partial_student_list.html', context)
        data['html_student_pagination'] = render_to_string('student/includes/partial_student_pagination.html', context)
        return JsonResponse(data)
    context = {'students':page_obj_students, 'courses':courses, 'session_years':session_years}
    return render(request, 'student/manage_student.html', context)

@csrf_exempt
def paginate_student(request):
    """
    Paginate all students of current adminhod's courses.
    """
    # get list of all courses' ids of current adminhod.
    courses_ids_list = Course.objects.filter(adminhod__user__id=request.user.id).values_list('id', flat=True)
    # get all students of current adminhod's courses. 
    students_qs = Student.objects.filter(course__id__in=courses_ids_list).order_by('course')
    # get page number of paginator.
    page_number = request.GET.get('page').split('&')[0]
    # get course id.
    course_id = request.GET.get('course_id')
    # get session year id.
    session_year_id = request.GET.get('session_year_id')
    # get student gender.
    gender = request.GET.get('gender')
    # get list of submitted data.
    list_data = [course_id, session_year_id, gender]
    data = dict()
    # paginate the search results.
    if request.GET.get('search'):
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        # filter students of current adminhod  by name or email, ordered alphabetically by name.
        students = search(q, students_qs)
        # paginate the students list.
        page_obj_students = paginate(students, page_number)
    # paginate the filter results.
    elif any(list_data):
        students = filter_students(
            course_id=course_id, 
            session_year_id=session_year_id, 
            gender=gender, 
            courses_ids_list=courses_ids_list
        )
        # paginate the students list.
        page_obj_students = paginate(students, page_number)
    else:
        # paginate the students list.
        page_obj_students = paginate(students_qs, page_number)    
    context = {'students':page_obj_students, 'request':request}
    data['html_student_list'] = render_to_string('student/includes/partial_student_list.html', context)
    data['html_student_pagination'] = render_to_string('student/includes/partial_student_pagination.html', context)    
    return JsonResponse(data)

@csrf_exempt
def filter_student(request):
    """
    Filter students by Course, Session or Gender.
    """
    # get course id.
    course_id = request.POST.get('course_id')
    # get session year id.
    session_year_id = request.POST.get('session_year_id')
    # get student gender.
    gender = request.POST.get('gender')
    # get list of all courses' ids of current adminhod.
    courses_ids_list = Course.objects.filter(adminhod__user__id=request.user.id).values_list('id', flat=True)
    data = dict()
    # filter students by Course, Session or Gender.
    students_qs = filter_students(
        course_id=course_id, 
        session_year_id=session_year_id, 
        gender=gender, 
        courses_ids_list=courses_ids_list
    )    
    if students_qs:
        # paginate the students list.
        page_obj_students = paginate(students_qs)
        context = {'students':page_obj_students, 'request':request}
    else:
        context = {'students':students_qs, 'request':request}          
    data['html_student_list'] = render_to_string('student/includes/partial_student_list.html', context)
    data['html_student_pagination'] = render_to_string('student/includes/partial_student_pagination.html', context)    
    return JsonResponse(data)
    
def update_student(request, student_id):
    """
    Take student's id, and get this student by its id.
    Update this student.
    """
    # get student by its id.
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        student_form = UpdateStudentAdminForm(request.POST, request.FILES, request=request, instance=student)
    else:
        student_form = UpdateStudentAdminForm(request=request, instance=student, initial={'course': student.course})
    return update_staff_student_form(request, student_form, 'student/includes/partial_student_update.html', student)

def delete_student(request, student_id):
    """
    Take student's id, and get this student by its id.
    Delete this student.
    """
    # get student by its id
    student = get_object_or_404(Student, pk=student_id)
    data = dict()
    if request.method == 'POST':
        data['student_name'] = student.user.full_name
        # delete student.
        student.delete()
        data['form_is_valid'] = True 
        data['is_update'] = False 
        students = Student.objects.all()
        data['html_student_list'] = render_to_string('student/includes/partial_student_list.html', {'students': students})
    else:
        context = {'student': student}
        data['html_form'] = render_to_string('student/includes/partial_student_delete.html', context, request=request)
    return JsonResponse(data)    
