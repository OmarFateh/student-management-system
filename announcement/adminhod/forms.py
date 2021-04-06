from django import forms

from announcement.models import Announcement

class AddAnnouncementForm(forms.ModelForm):
    """
    Add announcement model form.
    """
    header = forms.CharField(
        label='', 
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control', 
            'name':'header', 
            'placeholder':"Header",
        })
    )
    content = forms.CharField(
        label='', 
        widget=forms.Textarea(attrs={
            'class':'form-control',
            'rows':'6', 
            'name':'content', 
            'placeholder':"Add an Announcement ...",
            'style':"resize: none",
            'required': True,
        })
    )

    class Meta:
        model  = Announcement
        fields = ['header', 'content']