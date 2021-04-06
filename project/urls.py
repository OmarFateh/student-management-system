"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

from accounts.forms import (
        EmailValidationOnForgotPassword, 
        PasswordFieldsOnForgotPassword, 
        # PasswordFieldsOnChangePassword,
    )
from accounts.views import CustomPasswordResetConfirmView     

urlpatterns = [
    ## standard admin
    path('admin/', admin.site.urls),

    ## Regular Endpoints
    path('', include(('accounts.urls', 'accounts'), namespace='accounts')),
    # adminHOD
    path('', include(('adminhod.urls', 'adminhod'), namespace='adminhod')),
    # Course
    path('', include(('course.urls', 'course'), namespace='course')),
    # Staff
    path('', include(('staff.urls', 'staff'), namespace='staff')),
    # Student 
    path('', include(('student.urls', 'student'), namespace='student')),
    # Posts
    path('', include(('posts.urls', 'posts'), namespace='posts')),
    # Attendance
    path('', include(('attendance.adminhod.urls', 'attendance'), namespace='attendance-adminhod')),
    path('', include(('attendance.staff.urls', 'attendance'), namespace='attendance-staff')),
    path('', include(('attendance.student.urls', 'attendance'), namespace='attendance-student')),
    # Feedback
    path('', include(('feedback.adminhod.urls', 'feedback'), namespace='feedback-adminhod')),
    path('', include(('feedback.staff.urls', 'feedback'), namespace='feedback-staff')),
    path('', include(('feedback.student.urls', 'feedback'), namespace='feedback-student')),
    # Result
    path('', include(('result.adminhod.urls', 'result'), namespace='result-adminhod')),
    path('', include(('result.staff.urls', 'result'), namespace='result-staff')),
    path('', include(('result.student.urls', 'result'), namespace='result-student')),
    # Announcement
    path('', include(('announcement.adminhod.urls', 'announcement'), namespace='announcement-adminhod')),
    path('', include(('announcement.staff.urls', 'announcement'), namespace='announcement-staff')),
    path('', include(('announcement.student.urls', 'announcement'), namespace='announcement-student')),
    # Assignment
    path('', include(('assignment.adminhod.urls', 'assignment'), namespace='assignment-adminhod')),
    path('', include(('assignment.staff.urls', 'assignment'), namespace='assignment-staff')),
    path('', include(('assignment.student.urls', 'assignment'), namespace='assignment-student')),
    # Contact
    # path('', include(('contact.adminhod.urls', 'contact'), namespace='contact-adminhod')),
    path('', include(('contact.staff.urls', 'contact'), namespace='contact-staff')),
    path('', include(('contact.student.urls', 'contact'), namespace='contact-student')),
    # Feed
    # path('', include(('feed.adminhod.urls', 'feed'), namespace='feed-adminhod')),
    path('', include(('feed.staff.urls', 'feed'), namespace='feed-staff')),
    path('', include(('feed.student.urls', 'feed'), namespace='feed-student')),
    

    # Password reset
    # 1- Submit password form                     // PasswordResetView.as_view() 
    # 2- Email sent success message               // PasswordResetDoneView.as_view()  
    # 3- Link to password reset form in email     // PasswordResetConfirmView.as_view() 
    # 4- password successfully changed message    // PasswordResetCompleteView.as_view()

    path('password/reset/', auth_views.PasswordResetView.as_view(
                                template_name='accounts/password_reset.html',
                                form_class=EmailValidationOnForgotPassword,),
                                name='password_reset'),
    path('password/reset/sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html',), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    #                             template_name='accounts/password_reset_form.html',
    #                             form_class=PasswordFieldsOnForgotPassword,),
    #                             name='password_reset_confirm'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),                            
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html',), name='password_reset_complete'),

    # Password change
    # path('password_change/', auth_views.PasswordChangeView.as_view(
    #                             template_name='accounts/password_change_form.html',
    #                             form_class=PasswordFieldsOnChangePassword,),
    #                             name='password_change'),
    # path('password_change_complete/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html',), name='password_change_done'),
                            
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)