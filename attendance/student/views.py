import json
import datetime

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 

from course.models import Subject
from student.models import Student
from attendance.models import Attendance, AttendanceReport

# View Attendance
def view_attendance(request):
    """
    Display all attendance data of current student. 
    """
    # get current student.
    student = get_object_or_404(Student, user__id=request.user.id)
    # get all subjects of current student's course.
    subjects = Subject.objects.filter(course=student.course)
    context = {'subjects':subjects}
    return render(request, 'student/view_attendance.html', context)

@csrf_exempt
def get_attendance_data(request):
    """
    Get all attendance data for certain student and subject between range of two dates.
    """ 
    # current student.
    student = get_object_or_404(Student, user__id=request.user.id)   
    # get subject.
    subject_id = request.POST.get('subject_id')
    subject = get_object_or_404(Subject, id=subject_id)
    # get date range.
    date_range_str = request.POST.get('date_range')
    start_date = datetime.datetime.strptime(date_range_str[:10], '%m/%d/%Y').date()
    end_date = datetime.datetime.strptime(date_range_str[13:], '%m/%d/%Y').date()
    # get attendance record of this subject and attendance date.
    attendance = Attendance.objects.filter(attendance_date__range=(start_date, end_date), subject=subject)
    # get list of attendance report data of current student.
    attendance_reports_list_data = AttendanceReport.objects.get_attendance_reports_list_data(attendance, student)
    return JsonResponse(json.dumps(attendance_reports_list_data), content_type='application/json', safe=False)
