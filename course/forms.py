from django import forms

from adminhod.staff.forms import DateInputWidget
from staff.models import Staff
from adminhod.models import AdminHOD
from .models import Course, Subject

class BaseAddCourseSubjectForm(forms.ModelForm):
    """
    Base add Course Subject model form.
    """
    name = forms.CharField(
        label='', 
        max_length=255,
        widget=forms.TextInput(attrs={
            'class':'form-control', 
            'name':'name', 
            'placeholder':"Name",
            'required': True,
        })
    )
    code = forms.CharField(
        label='', 
        max_length=64,
        widget=forms.TextInput(attrs={
            'class':'form-control', 
            'name':'code', 
            'placeholder':"Code",
            'required': True,
        })
    )
    start_date = forms.DateField(widget=DateInputWidget(attrs={
            'class': 'form-control float-right',
            'placeholder':'dd/mm/yyyy',
            'required': True,
        })
    )
    end_date = forms.DateField(widget=DateInputWidget(attrs={
            'class': 'form-control float-right',
            'placeholder':'dd/mm/yyyy',
            'required': True,
        })
    )
    

class AddCourseForm(BaseAddCourseSubjectForm):
    """
    Add Course model form.
    """
    adminhod = forms.ModelChoiceField(
        queryset=AdminHOD.objects.all(),
        empty_label="Select AdminHOD",
        widget=forms.Select(attrs={
            'class':"form-control select2", 
            'name':'adminhod', 
            'style':"width: 100%",
            'required': True,
        })
    )
    class Meta:
        model  = Course
        fields = ['name', 'code', 'adminhod', 'start_date', 'end_date']
    
class AddSubjectForm(BaseAddCourseSubjectForm):
    """
    Add Subject model form.
    """
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        to_field_name='name',
        empty_label="Select Course",
        widget=forms.Select(attrs={
            'class':"form-control select2", 
            'name':'course', 
            'style':"width: 100%",
            'required': True,
        })
    )
    staff = forms.ModelChoiceField(
        queryset=Staff.objects.all(),
        empty_label="Select Staff",
        widget=forms.Select(attrs={
            'class':"form-control select2", 
            'name':'staff', 
            'style':"width: 100%",
            'required': True,
        })
    )
    class Meta:
        model  = Subject
        fields = ['name', 'code', 'course', 'staff', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(AddSubjectForm, self).__init__(*args, **kwargs)
        self.fields["course"].queryset = Course.objects.filter(adminhod__user__id=self.request.user.id)     