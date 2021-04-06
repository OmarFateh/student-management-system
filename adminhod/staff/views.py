from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.mail import EmailMessage, BadHeaderError
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt 

from accounts.forms import UserAddForm, UpdateUserForm
from accounts.models import User 
from accounts.utils import unique_password_generator
from student.models import Student
from staff.models import Staff
from course.models import Course, Subject
from adminhod.utils import search, paginate 
from .forms import AddStaffForm, UpdateStaffAdminForm
from .utils import filter_staffs

def add_staff_student_form(request, form, template_name, user_type):
    """
    Take form, template name, and user's type.
    Add staff in case of taking user's type is staff.
    Add student in case of taking user's type is student.
    """
    # display user form.
    user_form = UserAddForm(request.POST or None)
    is_admin = True
    # check if the request method is post.
    if request.method == "POST":
        # if the user form and profile form are valid.
        if user_form.is_valid() and form.is_valid():
            # fetch submitted data.
            full_name = user_form.cleaned_data.get("full_name")
            email = user_form.cleaned_data.get("email")
            # generate unique password.
            password = unique_password_generator()
            # create new user.
            new_user = User.objects.create(
                full_name = full_name,
                email = email,
                user_type = user_type,
            )
            new_user.set_password(password)
            new_user.save()
            # send email to new user with email and password.
            # EmailMessage( subject, message, email_from, recipient_list )
            try:
                email = EmailMessage(
                    f'Welcome {full_name} to Student Management System', # subject  
                    f"""Hello {full_name}, 
                    \n \nyour account has been added successfully to Student Management System,
                    and here is your data: 
                    \nEmail: {email} \nPassword: {password}\n \n \n \nBest Regards \nStudent Management System Team""", # message
                    'fatehomar0@gmail.com', # from email
                    [email,] # to email list
                )
                email.send(fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')  
            # create new student.
            if user_type == 'STUDENT':
                new_user.student.course = form.cleaned_data.get("course")
                new_user.student.photo = form.cleaned_data.get("photo")
                new_user.student.birth_date = form.cleaned_data.get("birth_date")
                new_user.student.nationality = form.cleaned_data.get("nationality")
                new_user.student.phone = form.cleaned_data.get("phone")
                new_user.student.address = form.cleaned_data.get("address")
                new_user.student.gender = form.cleaned_data.get("gender")
                new_user.student.session_year = form.cleaned_data.get("session_year")
                new_user.student.save()
                # Display success message.
                messages.success(request, f'New student "{full_name}" has been added successfully.', extra_tags='add-student')
                # if save and add another.
                if 'save_and_add_another' in request.POST:
                    # redirect to add students url.
                    return redirect('adminhod:add-student')
                # if save.
                elif 'save' in request.POST:
                    # redirect to manage students url.
                    return redirect('adminhod:manage-student')
            # create new staff.
            elif user_type == 'STAFF':
                new_user.staff.photo = form.cleaned_data.get("photo")
                new_user.staff.birth_date = form.cleaned_data.get("birth_date")
                new_user.staff.nationality = form.cleaned_data.get("nationality")
                new_user.staff.phone = form.cleaned_data.get("phone")
                new_user.staff.address = form.cleaned_data.get("address")
                new_user.staff.gender = form.cleaned_data.get("gender")
                new_user.staff.recruitment_date = form.cleaned_data.get("recruitment_date")
                new_user.staff.save()
                # Display success message.
                messages.success(request, f'New Staff "{full_name}" has been added successfully.', extra_tags='add-staff')
                # if save and add another.
                if 'save_and_add_another' in request.POST:
                    # redirect to add staff url.
                    return redirect('adminhod:add-staff')
                # if save.
                elif 'save' in request.POST:
                    # redirect to manage staff url.
                    return redirect('adminhod:manage-staff')

    context = {'is_admin':is_admin, 'user_form':user_form, 'form':form}
    return render(request, template_name, context)

def update_staff_student_form(request, form, template_name, staff_student):
    """
    Take form, template name, and staff or student.
    Update staff in case of taking staff.
    Update student in case of taking student.
    """
    # display initial data of student or staff.
    user_form = UpdateUserForm(
        request.POST or None,
        staff_student=staff_student, 
        instance=staff_student, 
        initial={'full_name': staff_student.user.full_name,
                 'email': staff_student.user.email, 
        })
    data = dict()
    is_update = True
    is_admin = True
    staff_student_name = staff_student.user.full_name
    if request.method == 'POST':
        if user_form.is_valid() and form.is_valid():
            # update student or staff.
            form.save()
            staff_student.user.full_name = user_form.cleaned_data.get('full_name')
            staff_student.user.email = user_form.cleaned_data.get('email')
            staff_student.user.save()
            staff_student.photo = form.cleaned_data.get('photo')
            staff_student.save()
            data['form_is_valid'] = True
            data['is_update'] = True
            # update student.
            if staff_student.user.user_type == 'STUDENT':
                # get all students.
                students = Student.objects.all()
                data['html_student_list'] = render_to_string('student/includes/partial_student_list.html', {'students': students})
                data['student_name'] = staff_student_name
            # update staff.    
            elif staff_student.user.user_type == 'STAFF': 
                # get all staffs.  
                staffs = Staff.objects.all()
                data['html_staff_list'] = render_to_string('staff/includes/partial_staff_list.html', {'staffs': staffs})
                data['staff_name'] = staff_student_name
        else:
            data['form_is_valid'] = False
    context = {'is_update':is_update, 'is_admin':is_admin, 'user_form':user_form, 'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def add_staff(request):
    """
    Add staff.
    """
    user_type = 'STAFF'
    if request.method == 'POST':
        staff_form = AddStaffForm(request.POST, request.FILES)
    else:
        staff_form = AddStaffForm()
    return add_staff_student_form(request, staff_form, 'staff/add_staff.html', user_type)

def manage_staff(request):
    """
    Display all staffs of current adminhod's courses.
    Search staff by name or email, ordered alphabetically by name.
    """    
    # get list of all staffs' ids of current adminhod's courses.
    staffs_ids_list = Subject.objects.staff_ids(request.user)
    # get all staffs of current adminhod's courses.
    staffs_qs = Staff.objects.filter(user__id__in=staffs_ids_list)
    # get all courses of current adminhod.
    courses = Course.objects.filter(adminhod__user__id=request.user.id)
    # paginate the staffs list.
    page_obj_staffs = paginate(staffs_qs)
    if request.is_ajax():
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        data = dict()  
        # filter staff by name or email, ordered alphabetically by name.
        staffs = search(q, staffs_qs)
        # paginate the staffs list.
        page_obj_staffs = paginate(staffs)    
        context = {'staffs': page_obj_staffs, 'request':request}
        data['html_staff_list'] = render_to_string('staff/includes/partial_staff_list.html', context)
        data['html_staff_pagination'] = render_to_string('staff/includes/partial_staff_pagination.html', context)
        return JsonResponse(data)
    context = {'staffs':page_obj_staffs, 'courses':courses}
    return render(request, 'staff/manage_staff.html', context)

def paginate_staff(request):
    """
    Paginate all staffs of current adminhod's courses.
    """
    # get list of all staffs' ids of current adminhod's courses.
    staffs_ids_list = Subject.objects.staff_ids(request.user)
    # get all staffs of current adminhod's courses.
    staffs_qs = Staff.objects.filter(user__id__in=staffs_ids_list)
    # get page number of paginator.
    page_number = request.GET.get('page').split('&')[0]
    # get course id.
    course_id = request.GET.get('course_id')
    # get student gender.
    gender = request.GET.get('gender')
    # get list of submitted data.
    list_data = [course_id, gender]
    data = dict()
    # paginate the search results.
    if request.GET.get('search'):
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        # filter staff by name or email, ordered alphabetically by name.
        staffs = search(q, staffs_qs)
        # paginate the staffs list.
        page_obj_staffs = paginate(staffs, page_number)
    # paginate the filter results.
    elif any(list_data):
        staffs = filter_staffs(
            course_id=course_id, 
            gender=gender, 
            staffs_ids_list=staffs_ids_list
        )
        # paginate the staffs list.
        page_obj_staffs = paginate(staffs, page_number)    
    else:
        # paginate the staffs list.
        page_obj_staffs = paginate(staffs_qs, page_number)    
    context = {'staffs':page_obj_staffs, 'request':request}
    data['html_staff_list'] = render_to_string('staff/includes/partial_staff_list.html', context)
    data['html_staff_pagination'] = render_to_string('staff/includes/partial_staff_pagination.html', context)    
    return JsonResponse(data)

@csrf_exempt
def filter_staff(request):
    """
    Filter staffs by Course or Gender.
    """
    # get course id.
    course_id = request.POST.get('course_id')
    # get staff gender.
    gender = request.POST.get('gender')
    # get list of all staffs' ids of current adminhod's courses.
    staffs_ids_list = Subject.objects.staff_ids(request.user)
    # get list of staff data.
    data = dict()
    # filter staffs by Course or Gender.
    staffs_qs = filter_staffs(
        course_id=course_id,  
        gender=gender, 
        staffs_ids_list=staffs_ids_list
    )    
    if staffs_qs:
        # paginate the staffs list.
        page_obj_staffs = paginate(staffs_qs)
        context = {'staffs':page_obj_staffs, 'request':request}
    else:
        context = {'staffs':staffs_qs, 'request':request}        
    data['html_staff_list'] = render_to_string('staff/includes/partial_staff_list.html', context)
    data['html_staff_pagination'] = render_to_string('staff/includes/partial_staff_pagination.html', context)    
    return JsonResponse(data)

def update_staff(request, staff_id):
    """
    Take staff's id, and get this staff by its id.
    Update this staff.
    """
    # get staff by its id.
    staff = get_object_or_404(Staff, pk=staff_id)
    if request.method == 'POST':
        staff_form = UpdateStaffAdminForm(request.POST, request.FILES, instance=staff)
    else:
        staff_form = UpdateStaffAdminForm(instance=staff)
    return update_staff_student_form(request, staff_form, 'staff/includes/partial_staff_update.html', staff)

def delete_staff(request, staff_id):
    """
    Take staff's id, and get this staff by its id.
    Delete this staff.
    """
    # get staff by its id
    staff = get_object_or_404(Staff, pk=staff_id)
    data = dict()
    if request.method == 'POST':
        data['staff_name'] = staff.user.full_name
        # delete staff.
        staff.delete()
        data['form_is_valid'] = True 
        data['is_update'] = False 
        staffs = Staff.objects.all()
        data['html_staff_list'] = render_to_string('staff/includes/partial_staff_list.html', {'staffs': staffs})
    else:
        context = {'staff': staff}
        data['html_form'] = render_to_string('staff/includes/partial_staff_delete.html', context, request=request)
    return JsonResponse(data) 