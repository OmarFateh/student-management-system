from django import forms

from assignment.models import StudentAssignment


class UploadAssignmentform(forms.ModelForm):
    """
    Upload assignment document model form.
    """
    document = forms.FileField(widget=forms.FileInput(attrs={'class':'custom-file-input', 'id':'fileInputAssignment', 'required': True,}))
    class Meta:
        model = StudentAssignment 
        fields = ['document', 'assignment', 'student']