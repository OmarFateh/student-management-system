import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 

from course.models import Course, Subject
from student.models import SessionYear
from result.models import StudentResult

# View Results
def view_results_adminhod(request):
    """
    Display all results data of current adminhod's courses.
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
    return render(request, 'adminhod/view_results.html', context)

@csrf_exempt
def get_results_data_adminhod(request):
    """
    Get all results data for certain subject and session year.
    """ 
    # get session year id.
    session_year_id = request.POST.get('session_year_id')   
    # get subject id.
    subject_id = request.POST.get('subject_id')
    # get list of results students for certain subject and session year.
    results_students_list_data = StudentResult.objects.get_results_students_list_data(subject_id, session_year_id)
    return JsonResponse(json.dumps(results_students_list_data), content_type='application/json', safe=False)
