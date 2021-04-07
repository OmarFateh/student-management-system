from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

from student.models import Student 
from course.models import Course, Subject
from attendance.models import Attendance, AttendanceReport
from feedback.models import FeedbackStudent
from posts.models import Post
from accounts.forms import UpdateUserForm
from adminhod.student.forms import UpdateStudentForm
from posts.utils import paginate_posts
from posts.forms import CommentForm


def student_dashboard(request):
    """
    Student dashboard.
    """
    # get current student.
    student = get_object_or_404(Student, user__id=request.user.id)
    # get course of current student.
    course = get_object_or_404(Course, id=student.course.id)
    # get subjects count of current student.
    subjects = Subject.objects.filter(course=course)
    subjects_count = subjects.count()
    # get attendance reports of current student.
    attendance_total = AttendanceReport.objects.filter(student=student).count()
    attendance_present = AttendanceReport.objects.filter(student=student, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(student=student, status=False).count()
    subjects_name = []
    subjects_present = []
    subjects_absent = []
    for subject in subjects:
        attendance = Attendance.objects.filter(subject=subject, session_year=student.session_year)
        attendance_present_total = AttendanceReport.objects.filter(student=student, attendance__in=attendance, status=True).count()
        attendance_absent_total = AttendanceReport.objects.filter(student=student, attendance__in=attendance, status=False).count()
        subjects_name.append(subject.name)
        subjects_present.append(attendance_present_total)
        subjects_absent.append(attendance_absent_total)
    # get feedback of current student.
    feedback_total = FeedbackStudent.objects.filter(student=student).count()
    feedback_replied = FeedbackStudent.objects.filter(student=student, is_replied=True).count()
    feedback_unreplied = FeedbackStudent.objects.filter(student=student, is_replied=False).count()
    context = {
        'subjects_count':subjects_count,
        'attendance_total':attendance_total,
        'attendance_present':attendance_present,
        'attendance_absent':attendance_absent,
        'subjects_name':subjects_name,
        'subjects_present':subjects_present,
        'subjects_absent':subjects_absent,
        'feedback_total':feedback_total,
        'feedback_replied':feedback_replied,
        'feedback_unreplied':feedback_unreplied,
    }
    return render(request, 'student/dashboard.html', context)

def student_profile(request, student_slug):
    """
    Take student slug, get the profile of this student.
    Display his profile detail.
    Update his profile data.
    """
    # get current student by its slug.
    student = get_object_or_404(Student, slug=student_slug) 
    # check if the user is the owner of this profile to edit. 
    editable = False
    if request.user.is_authenticated and request.user == student.user:
        editable = True
    # display all student's posts.
    posts = Post.objects.filter(user__student=student).order_by('-created_at')
    # paginate student's posts.
    page_number = request.GET.get('page', 1)
    page_obj_posts = paginate_posts(posts, page_number) 
    # comment form.
    comment_form = CommentForm(auto_id=False)     
    # update student profile.
    is_update = True
    data = dict()
    # display student's initial data.
    user_form = UpdateUserForm(
        request.POST or None,
        staff_student=student,  
        instance=student,
        initial={'full_name': student.user.full_name,
                 'email': student.user.email, 
        })
    if request.method == 'POST':
        student_form = UpdateStudentForm(request.POST, request.FILES, instance=student)
        if user_form.is_valid() and student_form.is_valid():
            data['form_is_valid'] = True
            # update student.
            student_form.save()
            student.user.full_name = user_form.cleaned_data.get('full_name')
            student.user.email = user_form.cleaned_data.get('email')
            student.user.save()
            # Display success message.
            data['success_message'] = "Your profile has been updated successfully."
            data['html_form'] = render_to_string(
                'student/includes/partial_student_form.html', 
                {'is_update':is_update, 'user_form':user_form, 'form': student_form})
            if request.user == student.user:
                data['html_student_sidebar_data'] = render_to_string('student/dashboard_includes/student_sidebar_data.html', {'user':student.user})  
            data['html_student_data'] = render_to_string('student/includes/partial_student_profile.html', {'student':student})   
            return JsonResponse(data)
    else:
        student_form = UpdateStudentForm(instance=student)     
    context = {
        'student':student, 
        'editable':editable,
        'posts':page_obj_posts,
        'is_update':is_update, 
        'user_form':user_form, 
        'form': student_form,
        'comment_form':comment_form,
    }    
    return render(request, 'student/student_profile.html', context)           