import json

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt 

from course.models import Subject
from student.models import Student, SessionYear
from attendance.models import Attendance, AttendanceReport

# Take Attendance
def take_attendance(request):
    """
    Take attendance of students of current staff's subjects.
    """
    # get all subjects of current staff.
    subjects = Subject.objects.filter(staff__user__id=request.user.id) 
    # get all session years. 
    session_years = SessionYear.objects.all()
    context = {'subjects':subjects, 'session_years':session_years}
    return render(request, 'staff/take_attendance.html', context)

@csrf_exempt
def get_students(request):
    """
    Get list of students date of certain subject and session year.
    """
    # get subject.
    subject_id = request.POST.get('subject')
    subject = get_object_or_404(Subject, id=subject_id)
    # get session year id.
    session_year_id = request.POST.get('session_year') 
    # get list of students data.
    students_list_data = Student.objects.get_students_list_data(subject, session_year_id)
    return JsonResponse(json.dumps(students_list_data), content_type='application/json', safe=False)

@csrf_exempt
def save_attendance(request):
    """
    Save students' attendance data.
    """
    # get attendance date.
    attendance_date = request.POST.get('attendance_date')
    # get subject.
    subject_id = request.POST.get('subject')
    subject = get_object_or_404(Subject, id=subject_id)
    # get session year.
    session_year_id = request.POST.get('session_year')
    session_year = get_object_or_404(SessionYear, id=session_year_id)    
    # create new attendance report for each student.
    # get list of students ids.
    student_data = request.POST.get('student_data')
    try:
        # create new attendance record.
        attendance, created = Attendance.objects.get_or_create(subject=subject, session_year=session_year, attendance_date=attendance_date)
        if created:
            students = json.loads(student_data)
            for student in students:
                # get student by its id.
                student_obj = get_object_or_404(Student, id=student['id'])
                # create new attendance report for each student.
                AttendanceReport.objects.create(student=student_obj, status=student['status'], attendance=attendance)
            return HttpResponse('CREATED')
        else:
            return HttpResponse('EXISTS')    
    except:
        return HttpResponse('ERROR')    

# Manage Attendance
def manage_attendance(request):
    """
    Get all attendance data of current staff's subjects.
    """
    # get all subjects of current staff.
    subjects = Subject.objects.filter(staff__user__id=request.user.id)
    # get all session years. 
    session_years = SessionYear.objects.all()
    context = {'subjects':subjects, 'session_years':session_years}
    return render(request, 'staff/manage_attendance.html', context)

@csrf_exempt
def get_attendance_dates(request):
    """
    Get all attendance dates for certain subject and session year.
    """
    # get subject.
    subject_id = request.POST.get('subject')
    subject = get_object_or_404(Subject, id=subject_id)
    # get session year.
    session_year_id = request.POST.get('session_year')
    session_year = get_object_or_404(SessionYear, id=session_year_id) 
    # get list of attendance for this subject and session year.
    attendance_dates_list_data = Attendance.objects.get_attendance_dates_list_data(subject, session_year)
    return JsonResponse(json.dumps(attendance_dates_list_data), content_type='application/json', safe=False)

@csrf_exempt
def get_attendance_students(request):
    """
    Get list of attendance students for attendance record.
    """
    # get attendance record.
    attendance_id = request.POST.get('attendance_id')
    attendance = get_object_or_404(Attendance, id=attendance_id)
    # get list of attendance students for attendance record.
    attendance_students_list_data = AttendanceReport.objects.get_attendance_students_list_data(attendance)
    return JsonResponse(json.dumps(attendance_students_list_data), content_type='application/json', safe=False)

@csrf_exempt
def update_attendance(request):
    """
    Update attendance data of current staff's courses.
    """
    # get attendance record.
    attendance_id = request.POST.get('attendance_id')
    attendance = get_object_or_404(Attendance, id=attendance_id)
    # update attendance report for each student.
    # get list of students ids.
    student_data = request.POST.get('student_data')
    try:
        students = json.loads(student_data)
        for student in students:
            # get student by its id.
            student_obj = get_object_or_404(Student, id=student['id'])
            # update attendance report for each student.
            attendance_report = get_object_or_404(AttendanceReport, student=student_obj, attendance=attendance)
            attendance_report.status = student['status']
            attendance_report.save()
        return HttpResponse('Ok')
    except:
        return HttpResponse('ERROR')    