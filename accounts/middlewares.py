from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class RestrictionRolesMiddleWare(MiddlewareMixin):
    """
    Custom middleware to restirct user's roles.
    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        # get module name from view_func variable.
        modulename = view_func.__module__ # file name where the request has been sent to.
        user = request.user
        if user.is_authenticated:
            if user.user_type == 'HOD':
                if modulename not in [
                    'adminhod.views', 
                    'adminhod.staff.views', 
                    'adminhod.student.views', 
                    'accounts.views', 
                    'course.views',
                    'announcement.adminhod.views',
                    'assignment.adminhod.views',
                    'feedback.adminhod.views',
                    'attendance.adminhod.views',
                    'result.adminhod.views',
                    'django.views.static',
                    'django.contrib.auth.views',
                    "django.contrib.admin.sites",
                ]:
                    return redirect("adminhod:dashboard") 
            elif user.user_type == 'STAFF':
                if user.previously_logged_in:
                    if modulename not in [
                        'staff.views', 
                        'accounts.views', 
                        'announcement.staff.views',
                        'assignment.staff.views',
                        'feedback.staff.views',
                        'attendance.staff.views',
                        'result.staff.views',
                        'django.views.static',
                        'django.contrib.auth.views',
                    ]:
                        return redirect("staff:dashboard")
                else:    
                    if modulename not in [ 
                        'accounts.views', 
                        'django.views.static',
                        'django.contrib.auth.views',
                    ]: 
                        return redirect("accounts:password-change") 
            elif user.user_type == 'STUDENT':
                if user.previously_logged_in:
                    if modulename not in [
                        'student.views', 
                        'accounts.views', 
                        'announcement.student.views',
                        'assignment.student.views',
                        'feedback.student.views',
                        'attendance.student.views',
                        'result.student.views',
                        'django.views.static',
                        'django.contrib.auth.views',
                    ]:
                        return redirect("student:dashboard")
                else:
                    if modulename not in [ 
                        'accounts.views', 
                        'django.views.static',
                        'django.contrib.auth.views',
                    ]: 
                        return redirect("accounts:password-change")          
        else:
            if request.path == reverse("accounts:login") or modulename in ['django.contrib.auth.views', 'django.contrib.admin.sites']:
                pass
            else:    
                return redirect("accounts:login")