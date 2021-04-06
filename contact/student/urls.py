from django.urls import path

from .views import (
    # student
    student_classmates,
    paginate_student_classmates,
    # staff
    student_contact_staff,
    paginate_student_staff,
)

# namespace = 'contact-student'

urlpatterns = [
    # student
    path('student/contacts/', student_classmates, name='student-contacts'),
    path('ajax/student/contacts/paginate/', paginate_student_classmates, name='ajax-paginate-student-contacts'),
    # staff
    path('student/contacts/staff/', student_contact_staff, name='student-contacts-staff'),
    path('ajax/student/contacts/staff/paginate/', paginate_student_staff, name='ajax-paginate-student-contacts-staff'),
] 