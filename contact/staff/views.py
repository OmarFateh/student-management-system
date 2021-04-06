from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt 

from student.models import Student 
from staff.models import Staff
from course.models import Course, Subject
from contact.utils import search, paginate

# staff
def contact_staff(request):
    """
    Display all staffs of current staff's courses.
    Search all staffs of current staff's courses, by name or email.
    """
    # get list of all staffs' ids of current staff's courses.
    staff_ids_list = Subject.objects.staff_ids(request.user, is_staff=True)
    # get all staffs of current staff's courses, except current staff.
    staffs_qs = Staff.objects.filter(user__id__in=staff_ids_list).exclude(user__id=request.user.id)
    # get list of all courses' ids of current staff.
    courses_ids_list = Subject.objects.courses_ids(request.user)
    # get list of all courses of current staff.
    courses = Course.objects.filter(id__in=courses_ids_list)
    # paginate the staffs list.
    page_obj_staffs = paginate(staffs_qs)    
    if request.is_ajax():
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        data = dict()
        # filter all staffs of current staff's courses, by name or email.
        staffs = search(q, staffs_qs)
        # paginate the staffs list.
        page_obj_staffs = paginate(staffs)  
        context = {'staffs':page_obj_staffs, 'request':request}
        data['html_staff_list'] = render_to_string('staff/includes/partial_contact_staff.html', context)
        return JsonResponse(data)
    context = {'staffs':page_obj_staffs, 'courses':courses}
    return render(request, 'staff/contact_staff.html', context)

def paginate_staff_contacts(request):
    """
    Paginate all staffs of current staff's courses.
    """
    # get list of all staffs' ids of current staff's courses.
    staff_ids_list = Subject.objects.staff_ids(request.user, is_staff=True)
    # get all staffs of current staff's courses, except current staff.
    staffs_qs = Staff.objects.filter(user__id__in=staff_ids_list).exclude(user__id=request.user.id)
    # get page number of paginator.
    page_number = request.GET.get('page').split('&')[0]
    # get course id.
    course_id = request.GET.get('course_id')
    data = dict()
    # paginate the search results.
    if request.GET.get('search'):
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        # filter all staffs of current student's course, by name or email.
        staffs = search(q, staffs_qs)
        # paginate the staffs list.
        page_obj_staffs = paginate(staffs, page_number) 
    elif course_id:
        # get list of all staffs' ids of selected course.
        staff_ids_list = Subject.objects.course_staffs_ids(course_id)
        # get all staffs of current staff's courses, except current staff.
        staffs = Staff.objects.filter(user__id__in=staff_ids_list).exclude(id=request.user.id)
        # paginate the staffs list.
        page_obj_staffs = paginate(staffs, page_number)
    else:
        # paginate the staffs list.
        page_obj_staffs = paginate(staffs_qs, page_number)   
    context = {'staffs':page_obj_staffs, 'request':request}
    data['html_staff_list'] = render_to_string('staff/includes/partial_contact_staff.html', context)
    return JsonResponse(data)

@csrf_exempt
def filter_staff_contacts(request):
    """
    Filter all staffs of current staff's courses by Course.
    """
    # get course id.
    course_id = request.POST.get('course_id')
    data = dict()
    if course_id:
        # get list of all staffs' ids of selected course.
        staff_ids_list = Subject.objects.course_staffs_ids(course_id)
    else:
        # get list of all staffs' ids of current staff's courses.
        staff_ids_list = Subject.objects.staff_ids(request.user, is_staff=True)
    # get all staffs of selected course, except current staff.
    staffs_qs = Staff.objects.filter(user__id__in=staff_ids_list).exclude(user__id=request.user.id)
    # paginate the staffs list.
    page_obj_staffs = paginate(staffs_qs)
    context = {'staffs':page_obj_staffs, 'request':request}
    data['html_staff_list'] = render_to_string('staff/includes/partial_contact_staff.html', context)
    return JsonResponse(data)

# student
def staff_contact_students(request):
    """
    Display all students of current staff's courses.
    Search all students of current staff's courses, by name or email.
    """
    # get list of all courses' ids of current staff.
    courses_ids_list = Subject.objects.courses_ids(request.user)
    # get all students of current staff's courses.
    students_qs = Student.objects.filter(course__id__in=courses_ids_list)
    # get list of all courses' ids of current staff.
    courses_ids_list = Subject.objects.courses_ids(request.user)
    # get list of all courses of current staff.
    courses = Course.objects.filter(id__in=courses_ids_list)
    # paginate the students list.
    page_obj_students = paginate(students_qs) 
    if request.is_ajax():
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        data = dict()
        # filter all students of current staff's courses, by name or email.
        students = search(q, students_qs)
        # paginate the students list.
        page_obj_students = paginate(students)    
        context = {'students': page_obj_students, 'request':request}
        data['html_students_list'] = render_to_string('staff/includes/partial_staff_contact_students.html', context)
        return JsonResponse(data)    
    context = {'students': page_obj_students, 'courses':courses}
    return render(request, 'staff/staff_contact_students.html', context) 

def paginate_staff_contacts_students(request):
    """
    Paginate all students of current staff's courses.
    """
    # get list of all courses' ids of current staff.
    courses_ids_list = Subject.objects.courses_ids(request.user)
    # get all students of current staff's courses.
    students_qs = Student.objects.filter(course__id__in=courses_ids_list)
    # get page number of paginator.
    page_number = request.GET.get('page').split('&')[0]
    # get course id.
    course_id = request.GET.get('course_id')
    data = dict()
    # paginate the search results.
    if request.GET.get('search'):
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        # filter all students of current staff's course, by name or email.
        students = search(q, students_qs)
        # paginate the students list.
        page_obj_students = paginate(students, page_number)
    elif course_id: 
        # get all students of selected course.
        students = Student.objects.filter(course__id=course_id) 
        # paginate the students list.
        page_obj_students = paginate(students, page_number)  
    else:
        # paginate the students list.
        page_obj_students = paginate(students_qs, page_number)     
    context = {'students':page_obj_students, 'request':request}
    data['html_students_list'] = render_to_string('staff/includes/partial_staff_contact_students.html', context)
    return JsonResponse(data)

@csrf_exempt
def filter_staff_contacts_students(request):
    """
    Filter all students of current staff's courses.
    """
    # get course id.
    course_id = request.POST.get('course_id')
    data = dict()
    if course_id:
        # get all students of selected course.
        students = Student.objects.filter(course__id=course_id)
    else:
        # get list of all courses' ids of current staff.
        courses_ids_list = Subject.objects.courses_ids(request.user)
        # get all students of current staff's courses.
        students = Student.objects.filter(course__id__in=courses_ids_list)
    # paginate the students list.
    page_obj_students = paginate(students)      
    context = {'students':page_obj_students, 'request':request}
    data['html_students_list'] = render_to_string('staff/includes/partial_staff_contact_students.html', context)
    return JsonResponse(data)
