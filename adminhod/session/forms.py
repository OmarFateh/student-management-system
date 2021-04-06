from django import forms

from student.models import SessionYear
# from adminhod.staff.forms import DateInputWidget

class AddSessionForm(forms.ModelForm):
    """
    Add session model form.
    """
    date_range = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control float-right js-validate-session',
            'placeholder':'dd/mm/yyyy',
            'required': True,
        })
    )
    
    class Meta:
        model = SessionYear
        fields = ['date_range']