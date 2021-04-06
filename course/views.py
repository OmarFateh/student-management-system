from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt 

from course.models import Course, Subject
from staff.models import Staff
from adminhod.utils import filter_list, paginate
from .utils import search, filter_subjects
from .forms import AddCourseForm, AddSubjectForm

def add_course_subject_form(request, form, template_name):
    """
    Take form and template name.
    Add course for in case of course. 
    Update subject for in case of subject.
    """
    # check if the request method is post.
    if request.method == "POST":
        # if the form is valid.
        if form.is_valid():
            name = form.cleaned_data.get("name")
            code = form.cleaned_data.get("code")
            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")
            # fetch submitted data and create new subject.
            if 'course' in request.POST:
                course = form.cleaned_data.get("course")
                staff = form.cleaned_data.get("staff")
                Subject.objects.create(
                    name=name,
                    code=code,
                    course=course,
                    staff=staff,
                    start_date=start_date,
                    end_date=end_date, 
                )
                # Display success message.
                messages.success(request, f'New subject "{name}" has been added successfully.', extra_tags='add-subject')
                # if save and add another.
                if 'save_and_add_another' in request.POST:
                    # redirect to add subjects url.
                    return redirect('course:add-subject')
                # if save.
                elif 'save' in request.POST:
                    # redirect to manage subjects url.
                    return redirect('course:manage-subject')
            # create new course.
            elif 'adminhod' in request.POST:
                adminhod = form.cleaned_data.get("adminhod")
                Course.objects.create(
                    name=name,
                    code=code,
                    adminhod=adminhod,
                    start_date=start_date,
                    end_date=end_date 
                )
                # Display success message.
                messages.success(request, f'New course "{name}" has been added successfully.', extra_tags='add-course')
                # if save and add another.
                if 'save_and_add_another' in request.POST:
                    # redirect to add courses url.
                    return redirect('course:add-course')
                # if save.
                elif 'save' in request.POST:
                    # redirect to manage courses url.
                    return redirect('course:manage-course')

    context = {'form':form}
    return render(request, template_name, context)

def add_course(request):
    """
    Add course.
    """
    if request.method == 'POST':
        course_form = AddCourseForm(request.POST)
    else:
        course_form = AddCourseForm()
    return add_course_subject_form(request, course_form, 'course/add_course.html')
 
def add_subject(request):
    """
    Add subject.
    """
    if request.method == 'POST':
        subject_form = AddSubjectForm(request.POST, request=request)
    else:
        subject_form = AddSubjectForm(request=request)
    return add_course_subject_form(request, subject_form, 'subject/add_subject.html')  

def manage_course(request):
    """
    Display all courses.
    Search courses by name or code, ordered alphabetically by course's name.
    """
    # get all courses.
    courses_qs = Course.objects.all()
    # paginate the courses list.
    page_obj_courses = paginate(courses_qs)
    if request.is_ajax():
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        data = dict()
        # filter courses by name or code, ordered alphabetically by course's name.
        courses = search(q, courses_qs)
        # paginate the courses list.
        page_obj_courses = paginate(courses)
        context = {'courses': page_obj_courses, 'request':request}
        data['html_course_list'] = render_to_string('course/includes/partial_course_list.html', context)
        data['html_course_pagination'] = render_to_string('course/includes/partial_course_pagination.html', context)
        return JsonResponse(data)    
    context = {'courses':page_obj_courses}
    return render(request, 'course/manage_course.html', context)

def paginate_course(request):
    """
    Paginate all courses.
    """
    # get all courses.
    courses_qs = Course.objects.all()
    # get page number of paginator.
    page_number = request.GET.get('page').split('&')[0]
    data = dict()
    # paginate the search results.
    if request.GET.get('search'):
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        # filter courses by name or code, ordered alphabetically by course's name.
        courses = search(q, courses_qs)
        # paginate the courses list.
        page_obj_courses = paginate(courses, page_number)
    else:
        # paginate the courses list.
        page_obj_courses = paginate(courses_qs, page_number)    
    context = {'courses':page_obj_courses, 'request':request}
    data['html_course_list'] = render_to_string('course/includes/partial_course_list.html', context)
    data['html_course_pagination'] = render_to_string('course/includes/partial_course_pagination.html', context)    
    return JsonResponse(data)

def manage_subject(request):
    """
    Display all subjects of current adminhod's courses.
    Search subjects of current adminhod's courses by name or code, ordered alphabetically by subject's name. 
    """
    # get all courses of current adminhod.
    courses = Course.objects.filter(adminhod__user__id=request.user.id)
    # get list of all staffs' ids of current adminhod's courses.
    staffs_ids_list = Subject.objects.staff_ids(request.user)
    # get all staffs of current adminhod's courses.
    staffs = Staff.objects.filter(user__id__in=staffs_ids_list)
    # get all subjects of current adminhod's courses, ordered alphabetically by course's name.
    subjects_qs = Subject.objects.filter(course__in=courses)
    # paginate the subjects list.
    page_obj_subjects = paginate(subjects_qs)
    if request.is_ajax():
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        data = dict()
        # filter subjects of current adminhod's courses by name or code, ordered alphabetically by subject's name.
        subjects = search(q, subjects_qs)
        # paginate the subjects list.
        page_obj_subjects = paginate(subjects)
        context = {'subjects': page_obj_subjects, 'request':request}
        data['html_subject_list'] = render_to_string('subject/includes/partial_subject_list.html', context)
        data['html_subject_pagination'] = render_to_string('subject/includes/partial_subject_pagination.html', context)
        return JsonResponse(data)    
    context = {'subjects':page_obj_subjects, 'courses':courses, 'staffs':staffs}
    return render(request, 'subject/manage_subject.html', context)

def paginate_subject(request):
    """
    Paginate all subjects of current adminhod's courses.
    """
    # get list all courses' ids of current adminhod.
    courses_ids_list = Course.objects.filter(adminhod__user__id=request.user.id).values_list('id', flat=True)
    # get all subjects of current adminhod's courses, ordered alphabetically by course's name.
    subjects_qs = Subject.objects.filter(course__id__in=courses_ids_list)
    # get page number of paginator.
    page_number = request.GET.get('page').split('&')[0]
    # get course id.
    course_id = request.GET.get('course_id')
    # get staff id.
    staff_id = request.GET.get('staff_id')
    list_data = [course_id, staff_id]
    data = dict()
    # paginate the search results.
    if request.GET.get('search'):
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        # filter subjects of current adminhod's courses by name or code, ordered alphabetically by subject's name.
        subjects = search(q, subjects_qs)
        # paginate the subjects list.
        page_obj_subjects = paginate(subjects, page_number)
    # paginate the filter results.
    elif any(list_data):
        subjects = filter_subjects(
            course_id=course_id, 
            staff_id=staff_id, 
            request=request, 
        )    
        # paginate the subjects list.
        page_obj_subjects = paginate(subjects, page_number) 
    else:
        # paginate the subjects list.
        page_obj_subjects = paginate(subjects_qs, page_number)    
    context = {'subjects':page_obj_subjects, 'request':request}
    data['html_subject_list'] = render_to_string('subject/includes/partial_subject_list.html', context)
    data['html_subject_pagination'] = render_to_string('subject/includes/partial_subject_pagination.html', context)    
    return JsonResponse(data)

@csrf_exempt
def filter_subject(request):
    """
    Filter subjects by Course or Staff.
    """
    # get course id.
    course_id = request.POST.get('course_id')
    # get staff id.
    staff_id = request.POST.get('staff_id')
    # get list of subject data.
    data = dict()
    # filter subjects by Course or Staff.
    subjects_qs = filter_subjects(
        course_id=course_id, 
        staff_id=staff_id, 
        request=request, 
    )    
    if subjects_qs:
        # paginate the subjects list.
        page_obj_subjects = paginate(subjects_qs)
        context = {'subjects':page_obj_subjects, 'request':request}
    else:
        context = {'subjects':subjects_qs, 'request':request}
    data['html_subject_list'] = render_to_string('subject/includes/partial_subject_list.html', context)
    data['html_subject_pagination'] = render_to_string('subject/includes/partial_subject_pagination.html', context)    
    return JsonResponse(data)

def update_course_subject_form(request, form, template_name, course_subject):
    """
    Take form, template name, and course or subject.
    Update course for in case of taking course. 
    Update subject for in case of taking subject. 
    """
    data = dict()
    course_subject_name = course_subject.name
    if request.method == 'POST':
        if form.is_valid():
            # update data for course or subject.
            course_subject.name = form.cleaned_data.get("name")
            course_subject.code = form.cleaned_data.get("code")
            course_subject.start_date = form.cleaned_data.get("start_date")
            course_subject.end_date = form.cleaned_data.get("end_date")
            course_subject.save()
            data['form_is_valid'] = True
            data['is_update'] = True
            # update subject.
            if 'course' in request.POST:
                course_subject.course = form.cleaned_data.get("course")
                course_subject.staff = form.cleaned_data.get("staff")
                course_subject.save()
                # get all subjects.
                subjects = Subject.objects.all()
                data['html_subject_list'] = render_to_string('subject/includes/partial_subject_list.html', {'subjects': subjects})
                data['subject_name'] = course_subject_name
            # update course.    
            else:  
                # get all courses.  
                courses = Course.objects.all()
                data['html_course_list'] = render_to_string('course/includes/partial_course_list.html', {'courses': courses})
                data['course_name'] = course_subject_name
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def update_course(request, course_id):
    """
    Take course's id, and get this course by its id.
    Update this course.
    """
    # get course by its id.
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        course_form = AddCourseForm(request.POST, instance=course)
    else:
        course_form = AddCourseForm(instance=course)
    return update_course_subject_form(request, course_form, 'course/includes/partial_course_update.html', course)
        
def update_subject(request, subject_id):
    """
    Take subject's id, and get this subject by its id.
    Update this subject.
    """
    # get subject by its id
    subject = get_object_or_404(Subject, pk=subject_id)
    if request.method == 'POST':
        subject_form = AddSubjectForm(request.POST, request=request, instance=subject)
    else:
        subject_form = AddSubjectForm(request=request, instance=subject, initial={'course': subject.course})
    return update_course_subject_form(request, subject_form, 'subject/includes/partial_subject_update.html', subject)

def delete_course(request, course_id):
    """
    Take course's id, and get this course by its id.
    Delete this course.
    """
    # get course by its id.
    course = get_object_or_404(Course, pk=course_id)
    data = dict()
    if request.method == 'POST':
        data['course_name'] = course.name 
        # delete course.
        course.delete()
        data['form_is_valid'] = True  
        data['is_update'] = False
        # get all courses.
        courses = Course.objects.all()
        data['html_course_list'] = render_to_string('course/includes/partial_course_list.html', {'courses': courses})
    else:
        context = {'course': course}
        data['html_form'] = render_to_string('course/includes/partial_course_delete.html', context, request=request)
    return JsonResponse(data)

def delete_subject(request, subject_id):
    """
    Take subject's id, and get this subject by its id.
    Delete this subject.
    """
    # get subject by its id.
    subject = get_object_or_404(Subject, pk=subject_id)
    data = dict()
    if request.method == 'POST':
        data['subject_name'] = subject.name
        # delete subject.
        subject.delete()
        data['form_is_valid'] = True
        data['is_update'] = False
        # get all subjects.
        subjects = Subject.objects.all()
        data['html_subject_list'] = render_to_string('subject/includes/partial_subject_list.html', {'subjects': subjects})
    else:
        context = {'subject': subject}
        data['html_form'] = render_to_string('subject/includes/partial_subject_delete.html', context, request=request)
    return JsonResponse(data)

