from django import forms

from course.models import Course, Subject

class AttendanceStudentForm(forms.Form):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.none()

        if 'course' in self.data:
            try:
                course_id = int(self.data.get('course'))
                self.fields['subject'].queryset = Subject.objects.filter(course=course_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Subject queryset
        elif self.instance.pk:
            self.fields['subject'].queryset = self.instance.course.subject_set.order_by('name')

    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        to_field_name='name',
        # empty_label="Select Course",
        widget=forms.Select(attrs={
            'class':"form-control",
            'id':'adminhod-view-attendance-course', 
            'name':'course', 
            'style':"width: 100%",
            'required': True,
        })
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        to_field_name='name',
        # empty_label="Select Subject",
        widget=forms.Select(attrs={
            'class':"form-control",
            'id':'adminhod-view-attendance-subject', 
            'name':'subject', 
            'style':"width: 100%",
            'required': True,
        })
    )
