from django.db import models

from course.models import Subject
from student.models import Student, SessionYear

class AttendanceManager(models.Manager):
    """
    Override the attendance manager.
    """
    def get_attendance_dates_list_data(self, subject, session_year):
        """
        """
        attendances = self.get_queryset().filter(subject=subject, session_year=session_year)
        attendance_dates_list_data = []
        if attendances.exists():
            for attendance in attendances:
                attendance_data = {'id':attendance.id, 'attendance_date':str(attendance.attendance_date)}
                attendance_dates_list_data.append(attendance_data)
        return attendance_dates_list_data           

class Attendance(models.Model):
    """
    Attendance model.
    """
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    session_year = models.ForeignKey(SessionYear, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = AttendanceManager()

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance'
        ordering = ['attendance_date']

    def __str__ (self):
        # Return user name.
        return f'{self.session_year} | {self.subject} | {self.attendance_date}'    

class AttendanceReportManager(models.Manager):
    """
    Override the attendance manager.
    """
    def get_attendance_students_list_data(self, attendance):
        """
        Take attendance object.
        Get list of students' attendance of this attendance object.
        """
        # get list of students' attendance of certain attendance object. 
        attendance_students = self.get_queryset().filter(attendance=attendance)
        attendance_students_list_data = []
        if attendance_students.exists():
            for attendance_student in attendance_students:
                attendance_students_data = {'id':attendance_student.student.id, 'name':attendance_student.student.user.full_name, 'status':attendance_student.status}
                attendance_students_list_data.append(attendance_students_data)
        return attendance_students_list_data 
    
    def get_attendance_reports_list_data(self, attendance, student):
        """
        Take student and attendance object.
        Get list of students' attendance reports of these student and attendance object. 
        """
        # get list of students' attendance reports of certain student and attendance object. 
        attendance_reports = self.get_queryset().filter(attendance__in=attendance, student=student)
        attendance_list_data = []
        if attendance_reports.exists():
            for attendance_report in attendance_reports:
                attendance_data = {'attendance_date':str(attendance_report.attendance.attendance_date), 'status':attendance_report.status}
                attendance_list_data.append(attendance_data)
        return attendance_list_data                         

class AttendanceReport(models.Model):
    """
    Attendance report model.
    """
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = AttendanceReportManager()

    class Meta:
        verbose_name = 'Attendance Report'
        verbose_name_plural = 'Attendance Reports'
        ordering = ['attendance__attendance_date']

    def __str__ (self):
        # Return user name.
        return self.student.user.full_name    