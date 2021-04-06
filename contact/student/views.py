from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string

from student.models import Student 
from staff.models import Staff
from course.models import Subject
from contact.utils import search, paginate

# students
def student_classmates(request):
    """
    Display all students of current student's course.
    Search all students of current student's course, by name or email.
    """
    # get all students of current student's course, except current student.
    students_qs = Student.objects.filter(course=request.user.student.course).exclude(user=request.user)
    # paginate the students list.
    page_obj_students = paginate(students_qs)    
    if request.is_ajax():
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        data = dict()
        # filter all students of current student's course, except current student, by name or email.
        students = search(q, students_qs)
        # paginate the students list.
        page_obj_students = paginate(students)    
        context = {'students': page_obj_students, 'request':request}
        data['html_student_classmates_list'] = render_to_string('student/includes/partial_student_classmates.html', context)
        return JsonResponse(data)    
    context = {'students': page_obj_students}
    return render(request, 'student/student_classmates.html', context)

def paginate_student_classmates(request):
    """
    Paginate all students of current student's course.
    """
    # get all students of current student's course, except current student.
    students_qs = Student.objects.filter(course=request.user.student.course).exclude(user=request.user)
    # get page number of paginator.
    page_number = request.GET.get('page').split('&')[0]
    data = dict()
    # paginate the search results.
    if request.GET.get('search'):
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        # filter all students of current student's course, except current student, by name or email.
        students = search(q, students_qs)
        # paginate the students list.
        page_obj_students = paginate(students, page_number)
    else:
        # paginate the students list.
        page_obj_students = paginate(students_qs, page_number)    
    context = {'students':page_obj_students, 'request':request}
    data['html_student_classmates_list'] = render_to_string('student/includes/partial_student_classmates.html', context)
    return JsonResponse(data)

# staff
def student_contact_staff(request):
    """
    Display all staffs of current student's course.
    Search all staffs of current student's course, by name or email.
    """
    # get list of all staffs' ids of current student's course.
    staff_ids_list = Subject.objects.staff_ids(request.user, is_student=True)
    # get all staffs of current student's course.
    staffs_qs = Staff.objects.filter(user__id__in=staff_ids_list)
    # paginate the staffs list.
    page_obj_staffs = paginate(staffs_qs) 
    if request.is_ajax():
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        data = dict()
        # filter all staffs of current student's course, by name or email.
        staffs = search(q, staffs_qs)
        # paginate the staffs list.
        page_obj_staffs = paginate(staffs)  
        context = {'staffs':page_obj_staffs, 'request':request}
        data['html_student_staff_list'] = render_to_string('student/includes/partial_student_contact_staff.html', context)
        return JsonResponse(data)
    context = {'staffs':page_obj_staffs}
    return render(request, 'student/student_contact_staff.html', context)

def paginate_student_staff(request):
    """
    Paginate all staffs of current student's course.
    """
    # get list of all staffs' ids of current student's course.
    staff_ids_list = Subject.objects.staff_ids(request.user, is_student=True)
    # get all staffs of current student's course.
    staffs_qs = Staff.objects.filter(id__in=staff_ids_list)
    # get page number of paginator.
    page_number = request.GET.get('page').split('&')[0]
    data = dict()
    # paginate the search results.
    if request.GET.get('search'):
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        # filter all staffs of current student's course, by name or email.
        staffs = search(q, staffs_qs)
        # paginate the staffs list.
        page_obj_staffs = paginate(staffs, page_number) 
    else:
        # paginate the staffs list.
        page_obj_staffs = paginate(staffs_qs, page_number)     
    context = {'staffs':page_obj_staffs, 'request':request}
    data['html_student_staff_list'] = render_to_string('student/includes/partial_student_contact_staff.html', context)
    return JsonResponse(data)