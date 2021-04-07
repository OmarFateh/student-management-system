from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from staff.models import Staff
from feedback.models import FeedbackStaff, FeedbackStudent
from course.models import Course, Subject
from student.models import Student
from accounts.forms import UpdateUserForm
from attendance.models import Attendance, AttendanceReport
from .models import AdminHOD


def admin_dashboard(request):
    """
    Adminhod dashboard.
    """
    # get count of all courses of current adminhod.
    courses = Course.objects.filter(adminhod__user__id=request.user.id)
    courses_total = courses.count()
    # get all subjects count.
    subjects_total = Subject.objects.user_subjects(request.user).count()
    # get all students count.
    students_total = Student.objects.filter(course__in=courses).count()
    # get list of all staffs' ids of current adminhod's courses.
    staffs_ids_list = Subject.objects.staff_ids(request.user)
    # get all staff count.
    staff_total = Staff.objects.filter(user__id__in=staffs_ids_list).count()
    # get all subjects count in each course.
    courses_name = []
    subjects_count = []
    students_count = []
    courses_present = []
    courses_absent = []
    for course in courses:
        # get all subjects count in each course.
        subjects_each_course = Subject.objects.filter(course=course)
        subjects_each_course_count = subjects_each_course.count()
        subjects_count.append(subjects_each_course_count)
        # get all students count in each course.
        students_each_course_count = Student.objects.filter(course=course).count()
        students_count.append(students_each_course_count)
        # # get attendance reports of each subject of each course.
        attendance = Attendance.objects.filter(subject__in=subjects_each_course)
        attendance_present_total = AttendanceReport.objects.filter(attendance__in=attendance, status=True).count()
        attendance_absent_total = AttendanceReport.objects.filter(attendance__in=attendance, status=False).count()
        courses_present.append(attendance_present_total)
        courses_absent.append(attendance_absent_total)
        # append name of each course to courses list.
        courses_name.append(course.name)    
    # get all staffs' feedbacks of current adminhod courses.    
    feedbacks_staff = FeedbackStaff.objects.filter(staff__id__in=staffs_ids_list)
    feedback_staff_total = feedbacks_staff.count()
    feedback_staff_replied = feedbacks_staff.filter(is_replied=True).count()
    feedback_staff_unreplied = feedbacks_staff.filter(is_replied=False).count()
    # get all student feedback.
    feedbacks_student = FeedbackStudent.objects.filter(student__course__in=courses)
    feedback_student_total = feedbacks_student.count()
    feedback_student_replied = feedbacks_student.filter(is_replied=True).count()
    feedback_student_unreplied = feedbacks_student.filter(is_replied=False).count()      
    context = {
        'courses_total':courses_total,
        'subjects_total':subjects_total,
        'students_total':students_total,
        'staff_total':staff_total,
        'courses_name':courses_name,
        'subjects_count':subjects_count,
        'students_count':students_count,
        'courses_present':courses_present,
        'courses_absent':courses_absent,
        'feedback_staff_total':feedback_staff_total,
        'feedback_staff_replied':feedback_staff_replied,
        'feedback_staff_unreplied':feedback_staff_unreplied,
        'feedback_student_total':feedback_student_total,
        'feedback_student_replied':feedback_student_replied,
        'feedback_student_unreplied':feedback_student_unreplied,
    }
    return render(request, 'adminhod/dashboard.html', context)

def update_adminhod_view(request):
    """
    Update profile of current adminhod.
    """
    # get current adminhod.
    adminhod = get_object_or_404(AdminHOD, user__id=request.user.id) 
    # display adminhod's initial data.
    user_form = UpdateUserForm(
        request.POST or None,
        staff_student=adminhod,  
        instance=adminhod,
        initial={'full_name': adminhod.user.full_name,
                 'email': adminhod.user.email, 
        })
    if request.method == 'POST':
        if user_form.is_valid():
            # update adminhod.
            adminhod.user.full_name = user_form.cleaned_data.get("full_name")
            adminhod.user.email = user_form.cleaned_data.get("email")
            adminhod.user.save()
            # Display success message.
            messages.success(request, f'Your profile has been updated successfully.', extra_tags='update-adminhod-profile')
            return redirect('adminhod:update-adminhod-profile') 
    context = {'user_form':user_form}
    return render(request, 'adminhod/update_adminhod_profile.html', context)