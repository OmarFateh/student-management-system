from django import forms

from student.models import Student, SessionYear
from course.models import Course
from adminhod.staff.forms import BaseAddStaffStudentForm

class AddStudentForm(BaseAddStaffStudentForm):
    """
    Add Student model form.
    """
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        empty_label="Select Course",
        widget=forms.Select(attrs={
            'class':"form-control select2", 
            'name':'course', 
            'style':"width: 100%",
            'required': True,
        })
    )
    session_year = forms.ModelChoiceField(
        queryset=SessionYear.objects.all(),
        empty_label="Select Session",
        widget=forms.Select(attrs={
            'class':"form-control select2", 
            'name':'session_year', 
            'style':"width: 100%",
            'required': True,
        })
    )
    
    class Meta:
        model  = Student
        fields = ['course', 'photo', 'nationality', 'phone', 'address', 'gender', 'birth_date', 'session_year']
        widgets = {'photo':forms.FileInput(
                attrs={'class':'custom-file-input', 'id':'fileInputStudent', 'required': True, } 
        )}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(AddStudentForm, self).__init__(*args, **kwargs)
        self.fields["course"].queryset = Course.objects.filter(adminhod__user__id=self.request.user.id)    

class UpdateStudentAdminForm(AddStudentForm):
    """
    Update Student Admin model form.
    """
    class Meta:
        model  = Student
        fields = ['course', 'photo', 'nationality', 'phone', 'address', 'gender', 'birth_date', 'session_year']
        widgets = {'photo':forms.FileInput(
                attrs={'class':'custom-file-input', 'id':'fileInputStudent'} 
        )}

class UpdateStudentForm(BaseAddStaffStudentForm):
    """
    Update Student model form.
    """
    photo = forms.FileField(widget=forms.FileInput(attrs={'class':'custom-file-input', 'id':'fileInputStudent'}))

    class Meta:
        model  = Student
        fields = ['photo', 'nationality', 'phone', 'address', 'gender', 'birth_date', 'education', 'skills']