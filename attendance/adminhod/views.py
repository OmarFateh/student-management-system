import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 

from course.models import Course, Subject
from student.models import SessionYear
from attendance.models import Attendance, AttendanceReport

# View Attendance
def view_attendance_adminhod(request):
    """
    Display all attendance data of current adminhod's courses.
    """
    # get all courses of current adminhod.
    courses = Course.objects.filter(adminhod__user__id=request.user.id)
    # get all session years.
    session_years = SessionYear.objects.all()
    # get first course.
    first_course = courses.first()
    # get all subjects of first course.
    subjects = Subject.objects.filter(course=first_course) 
    context = {'courses':courses, 'session_years':session_years, 'subjects':subjects}
    return render(request, 'adminhod/view_attendance.html', context)

def get_attendance_subjects(request):
    """
    Get all subjects of a selected course.
    """
    # get course id.
    course_id = request.GET.get('course')
    # check if staff assignment or not.
    is_staff_assignment = request.GET.get('is_staff_assignment')
    # get list of subjects data of current course.
    if course_id and is_staff_assignment:
        subjects_list_data = Subject.objects.get_subjects_list_data(course_id, is_staff_assignment=True)
    elif course_id:
        subjects_list_data = Subject.objects.get_subjects_list_data(course_id)
    else:
        subjects_list_data = Subject.objects.get_subjects_list_data()    
    return JsonResponse(json.dumps(subjects_list_data), content_type='application/json', safe=False) 

@csrf_exempt
def get_attendance_data_adminhod(request):
    """
    Get all attendance data for certain student and subject between range of two dates.
    """ 
    # get session year id.
    session_year_id = request.POST.get('session_id')   
    # get subject id.
    subject_id = request.POST.get('subject_id')
    # get attendance date.
    attendance_date = request.POST.get('attendance_date')
    # get attendance record of this subject, attendance date and session year.
    try:
        attendance = Attendance.objects.get(attendance_date=attendance_date, subject__id=subject_id, session_year__id=session_year_id)
    except:
        attendance = None
    # get list of attendance students for attendance record.
    attendance_students_list_data = AttendanceReport.objects.get_attendance_students_list_data(attendance)
    return JsonResponse(json.dumps(attendance_students_list_data), content_type='application/json', safe=False)
