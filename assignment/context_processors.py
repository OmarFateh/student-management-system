from assignment.models import Assignment

def assignments_count(request):
    """
    Custom context processor for assignments count.
    """
    count_assignments = 0
    # check if current user is authenticated or not.
    if request.user.is_authenticated:
        try:
            # get assignments count for students.
            student = request.user.student
            count_assignments = Assignment.objects.assignments_count(student)
        except:
            # get assignments count for adminhod.
            try: 
                if request.user.adminhod:
                    count_assignments = Assignment.objects.assignments_count()
            except:
                pass      
    return {'count_assignments':count_assignments} 