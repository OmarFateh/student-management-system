import json

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt 

from course.models import Subject
from student.models import Student, SessionYear
from result.models import StudentResult

def add_results(request):
    """
    Add results data.
    """
    # get all subjects of current staff.
    subjects = Subject.objects.filter(staff__user__id=request.user.id) 
    # get all session years.
    session_years = SessionYear.objects.all()
    context = {'subjects':subjects, 'session_years':session_years}
    return render(request, 'staff/add_results.html', context)

@csrf_exempt
def get_students_results(request):
    """
    Get all students of certain subject and session year.
    """
    # get subject.
    subject_id = request.POST.get('subject')
    subject = get_object_or_404(Subject, id=subject_id)
    # get session year id.
    session_year_id = request.POST.get('session_year')
    # get list of student date.
    is_results = True
    students_list_data = Student.objects.get_students_list_data(subject, session_year_id, is_results)
    return JsonResponse(json.dumps(students_list_data), content_type='application/json', safe=False) 

@csrf_exempt
def get_students_initial_results(request):
    """
    Get all results data for certain student, subject and session year.
    """ 
    # get student.
    student_id = request.POST.get('student_id') 
    student = get_object_or_404(Student, id=student_id)  
    # get subject id.
    subject_id = request.POST.get('subject_id')
    # get list of results students for certain student, subject and session year.
    initial_results_list_data = StudentResult.objects.get_results_list_data(student, subject_id)
    return JsonResponse(json.dumps(initial_results_list_data), content_type='application/json', safe=False)

@csrf_exempt
def save_results(request):
    """
    Save students' results data. 
    """
    # get student.
    student_id = request.POST.get('student_id')
    student = get_object_or_404(Student, id=student_id)
    # get subject.
    subject_id = request.POST.get('subject_id')
    subject = get_object_or_404(Subject, id=subject_id)
    # get session year.
    session_year_id = request.POST.get('session_year_id')
    session_year = get_object_or_404(SessionYear, id=session_year_id)
    # get assignment no.1 marks.
    assignment_one_marks = request.POST.get('assignment_one_marks')
    # get assignment no.2 marks.
    assignment_two_marks = request.POST.get('assignment_two_marks')
    # get assignment no.3 marks.
    assignment_three_marks = request.POST.get('assignment_three_marks')
    # get assignment no.4 marks.
    assignment_four_marks = request.POST.get('assignment_four_marks')
    # get assignment no.5 marks.
    assignment_five_marks = request.POST.get('assignment_five_marks')
    # get final exam marks.
    final_exam_marks = request.POST.get('final_exam_marks')
    try:
        # create new student result record.
        student_result, created = StudentResult.objects.get_or_create(student=student, subject=subject, session_year=session_year)
        if assignment_one_marks:
            student_result.assignment_one_marks = assignment_one_marks
        else:
            student_result.assignment_one_marks = None
        if assignment_two_marks: 
            student_result.assignment_two_marks = assignment_two_marks
        else:
            student_result.assignment_two_marks = None    
        if assignment_three_marks:
            student_result.assignment_three_marks = assignment_three_marks
        else:
            student_result.assignment_three_marks = None    
        if assignment_four_marks:    
            student_result.assignment_four_marks = assignment_four_marks
        else:
            student_result.assignment_four_marks = None    
        if assignment_five_marks:
            student_result.assignment_five_marks = assignment_five_marks
        else:
            student_result.assignment_five_marks = None    
        if final_exam_marks:    
            student_result.final_exam_marks = final_exam_marks
        else:
            student_result.final_exam_marks = None    
        student_result.save()
        return HttpResponse('OK')    
    except:
        return HttpResponse('ERROR') 