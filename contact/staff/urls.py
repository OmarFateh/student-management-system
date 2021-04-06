from django.urls import path

from .views import (
    # staff
    contact_staff,
    paginate_staff_contacts,
    filter_staff_contacts,
    # student
    staff_contact_students,
    paginate_staff_contacts_students,
    filter_staff_contacts_students,
)

# namespace = 'contact-staff'

urlpatterns = [
    # staff
    path('staff/contacts/', contact_staff, name='contacts-staff'),
    path('ajax/staff/contacts/paginate/', paginate_staff_contacts, name='ajax-paginate-contacts-staff'),
    path('ajax/staff/contacts/filter/', filter_staff_contacts, name='ajax-filter-contacts-staff'),
    # student
    path('staff/contacts/students/', staff_contact_students, name='staff-contacts-students'),
    path('ajax/staff/contacts/students/paginate/', paginate_staff_contacts_students, name='ajax-paginate-staff-contacts-students'),
    path('ajax/staff/contacts/students/filter/', filter_staff_contacts_students, name='ajax-filter-staff-contacts-students'),
]