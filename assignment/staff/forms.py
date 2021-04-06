from django import forms

from assignment.models import Assignment
from course.models import Subject
from student.models import SessionYear
from adminhod.staff.forms import DateInputWidget

class AddAssignmentform(forms.ModelForm):
    """
    Add assignment model form.
    """
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        empty_label="Select Subject",
        widget=forms.Select(attrs={
            'class':"form-control", 
            'name':'subject', 
            'style':"width: 100%",
            'required': True,
        })
    )
    session_year = forms.ModelChoiceField(
        queryset=SessionYear.objects.all(),
        empty_label="Select Session",
        widget=forms.Select(attrs={
            'class':"form-control", 
            'name':'session_year', 
            'style':"width: 100%",
            'required': True,
        })
    )
    content = forms.CharField(
        label='', 
        widget=forms.Textarea(attrs={
            'class':'form-control', 
            'name':'content', 
            'placeholder':"Write an Assignment ...",
            'row':6,
            'style':"resize: none;",
            'required': True,
        })
    )
    deadline_date = forms.DateField(widget=DateInputWidget(attrs={
            'class': 'form-control float-right',
            'name':'deadline_date',
            'placeholder':'dd/mm/yyyy',
            'id':'assignment-deadline-date',
            'required': True,
        })
    )
    allow_submission_after_deadline = forms.BooleanField(required=False)
    class Meta:
        model = Assignment 
        fields = ['subject', 'session_year', 'content', 'deadline_date', 'allow_submission_after_deadline']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(AddAssignmentform, self).__init__(*args, **kwargs)
        self.fields["subject"].queryset = Subject.objects.filter(staff__user__id=self.request.user.id)