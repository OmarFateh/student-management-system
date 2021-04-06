import json

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 

from course.models import Subject
from student.models import Student
from result.models import StudentResult

# View Results
def view_results(request):
    """
    Display all results data.
    """
    # get current student.
    student = get_object_or_404(Student, user__id=request.user.id)
    # get all subjects of current student's course.
    subjects = Subject.objects.filter(course=student.course)
    context = {'subjects':subjects}
    return render(request, 'student/view_results.html', context)

@csrf_exempt
def get_results_data(request):
    """
    Get all results data for certain student and subject.
    """ 
    # current student.
    student = get_object_or_404(Student, user__id=request.user.id)   
    # get subject.
    subject_id = request.POST.get('subject_id')
    # get list of results data of this subject for current student.
    results_list_data = StudentResult.objects.get_results_list_data(student, subject_id)
    return JsonResponse(json.dumps(results_list_data), content_type='application/json', safe=False)
