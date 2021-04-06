from django.db import models

class StudentResultManager(models.Manager):
    """
    """
    def get_results_students_list_data(self, subject_id, session_year_id):
        """
        """
        results_students = self.get_queryset().filter(subject__id=subject_id, session_year__id=session_year_id)
        results_students_list_data = []
        if results_students.exists():
            for results_student in results_students:
                results_students_data = {
                    'id':results_student.student.id, 
                    'name':results_student.student.user.full_name, 
                    'assignment_one_marks':results_student.assignment_one_marks,
                    'assignment_two_marks':results_student.assignment_two_marks,
                    'assignment_three_marks':results_student.assignment_three_marks,
                    'assignment_four_marks':results_student.assignment_four_marks,
                    'assignment_five_marks':results_student.assignment_five_marks,
                    'final_exam_marks':results_student.final_exam_marks,
                }
                results_students_list_data.append(results_students_data)
        return results_students_list_data

    def get_results_list_data(self, student, subject_id):
        """
        """
        results_students = self.get_queryset().filter(subject__id=subject_id, student=student)
        results_students_list_data = []
        if results_students.exists():
            for results_student in results_students:
                results_students_data = {
                    'assignment_one_marks':results_student.assignment_one_marks,
                    'assignment_two_marks':results_student.assignment_two_marks,
                    'assignment_three_marks':results_student.assignment_three_marks,
                    'assignment_four_marks':results_student.assignment_four_marks,
                    'assignment_five_marks':results_student.assignment_five_marks,
                    'final_exam_marks':results_student.final_exam_marks,
                }
                results_students_list_data.append(results_students_data)
        return results_students_list_data


class StudentResult(models.Model):
    """
    """
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey('course.Subject', on_delete=models.CASCADE)
    session_year = models.ForeignKey('student.SessionYear', on_delete=models.CASCADE)
    assignment_one_marks = models.FloatField(default=0, null=True, blank=True)
    assignment_two_marks = models.FloatField(default=0, null=True, blank=True)
    assignment_three_marks = models.FloatField(default=0, null=True, blank=True)
    assignment_four_marks = models.FloatField(default=0, null=True, blank=True)
    assignment_five_marks = models.FloatField(default=0, null=True, blank=True)
    final_exam_marks = models.FloatField(default=0, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = StudentResultManager()

    class Meta:
        verbose_name = 'Student Result'
        verbose_name_plural = 'Student Results'
        ordering = ['student__user__full_name']

    def __str__ (self):
        # Return student's name and subject's name.
        return f'{self.student.user.full_name} | {self.subject}'        
