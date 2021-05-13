from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

from staff.models import Staff
from announcement.models import Announcement
from feedback.models import FeedbackStaff
from course.models import Course, Subject
from student.models import Student
from attendance.models import Attendance, AttendanceReport
from posts.models import Post
from notifications.models import Notification
from accounts.forms import UpdateUserForm
from adminhod.staff.forms import UpdateStaffForm
from posts.utils import paginate_posts
from posts.forms import CommentForm


def staff_dashboard(request):
    """
    Staff dashboard.
    """
    # get current staff.
    staff = get_object_or_404(Staff, user__id=request.user.id)
    # get subjects count of current staff.
    subjects = Subject.objects.filter(staff=staff)
    subjects_count = subjects.count()
    # get list courses ids of current staff's subjects.
    courses_id_list = []
    for subject in subjects:
        course = get_object_or_404(Course, id=subject.course.id)
        courses_id_list.append(course.id)    
    # remove any duplicate course id.
    courses_id_distinct_list = list(set(courses_id_list))
    # get students count under current staff.
    students_count = Student.objects.filter(course__id__in=courses_id_distinct_list).count()
    # get attendance reports of each subject of current staff.
    subjects_name = []
    subjects_present = []
    subjects_absent = []
    for subject in subjects:
        attendance = Attendance.objects.filter(subject=subject)
        attendance_present_total = AttendanceReport.objects.filter(attendance__in=attendance, status=True).count()
        attendance_absent_total = AttendanceReport.objects.filter(attendance__in=attendance, status=False).count()
        subjects_name.append(subject.name)
        subjects_present.append(attendance_present_total)
        subjects_absent.append(attendance_absent_total)
    # get announcements count of current staff.
    announcements_total = Announcement.objects.filter(staff=staff).count()
    # get feedback of current staff.
    feedback_total = FeedbackStaff.objects.filter(staff=staff).count()
    feedback_replied = FeedbackStaff.objects.filter(staff=staff, is_replied=True).count()
    feedback_unreplied = FeedbackStaff.objects.filter(staff=staff, is_replied=False).count() 
    context = {
        'subjects_count':subjects_count,
        'students_count':students_count,
        'subjects_name':subjects_name,
        'subjects_present':subjects_present,
        'subjects_absent':subjects_absent,
        'announcements_total':announcements_total,
        'feedback_total':feedback_total,
        'feedback_replied':feedback_replied,
        'feedback_unreplied':feedback_unreplied,
    }
    return render(request, 'staff/dashboard.html', context)

def staff_profile(request, staff_slug):
    """
    Take staff slug, get the profile of this staff.
    Display his profile detail.
    Display his notifications.
    Update his profile data.
    """
    # get current staff by its slug.
    staff = get_object_or_404(Staff, slug=staff_slug) 
    # check if the user is the owner of this profile to edit. 
    editable = False
    if request.user.is_authenticated and request.user == staff.user:
        editable = True 
    # get all staff's posts.
    posts = Post.objects.filter(user__staff=staff).order_by('-created_at')  
    # paginate staff's posts.
    page_number = request.GET.get('page', 1)
    page_obj_posts = paginate_posts(posts, page_number) 
    # comment form.
    comment_form = CommentForm(auto_id=False) 
    # get staff notifications.
    notifications = Notification.objects.notifications_received(staff.user)
    # update staff notifications from not seen to seen. 
    Notification.objects.notifications_updated(staff.user)   
    # update staff profile.
    is_update = True
    data = dict()
    # display staff's initial data.
    user_form = UpdateUserForm(
        request.POST or None,
        staff_student=staff,  
        instance=staff,
        initial={'full_name': staff.user.full_name,
                 'email': staff.user.email, 
        })   
    if request.method == 'POST':
        staff_form = UpdateStaffForm(request.POST, request.FILES, instance=staff)
        if user_form.is_valid() and staff_form.is_valid():
            data['form_is_valid'] = True
            # update staff.
            staff_form.save()
            staff.user.full_name = user_form.cleaned_data.get('full_name')
            staff.user.email = user_form.cleaned_data.get('email')
            staff.user.save()
            # Display success message. 
            data['success_message'] = "Your profile has been updated successfully."
            data['html_form'] = render_to_string(
                'staff/includes/partial_staff_form.html', 
                {'is_update':is_update, 'user_form':user_form, 'form': staff_form})
            if request.user == staff.user:
                data['html_staff_sidebar_data'] = render_to_string('staff/dashboard_includes/staff_sidebar_data.html', {'user':staff.user})   
            data['html_staff_data'] = render_to_string('staff/includes/partial_staff_profile.html', {'staff':staff})   
            return JsonResponse(data)
    else:
        staff_form = UpdateStaffForm(instance=staff)     
    context = {
        'staff':staff, 
        'editable':editable,
        'posts':page_obj_posts,
        'is_update':is_update, 
        'user_form':user_form, 
        'form': staff_form,
        'comment_form':comment_form,
        'notifications':notifications,
    }    
    return render(request, 'staff/staff_profile.html', context)