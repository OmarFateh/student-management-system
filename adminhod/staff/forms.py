import re

from django import forms

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from staff.models import Staff


class DateInputWidget(forms.DateInput):
    """
    Custom date input widget. 
    """
    input_type = 'date'
    attrs = {'class': 'form-control float-right', 'placeholder':'dd/mm/yyyy', 'required': True,}

class BaseAddStaffStudentForm(forms.ModelForm):
    """
    Base add Staff Student model form.
    """
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    nationality = CountryField(blank_label='Select Country').formfield(
        label='',
        widget=CountrySelectWidget(attrs={
            "class": "form-control select2", 
            'name':'nationality', 
            'style':"width: 100%",
            'required': True,
        })
    )
    birth_date = forms.DateField(widget=DateInputWidget(attrs={
            'class': 'form-control float-right',
            'placeholder':'dd/mm/yyyy',
            'required': True,
        })
    )
    gender = forms.ChoiceField(
        label="", 
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={
            'class':"form-control select2", 
            'name':'gender', 
            'style':"width: 100%",
        })
    )
    phone = forms.CharField(
        label='', 
        max_length=17,
        widget=forms.TextInput(attrs={
            'class':'form-control', 
            'name':'phone', 
            'placeholder':"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
            'required': True,
        })
    )
    address = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={
            'class':'form-control', 
            'name':'address', 
            'placeholder':"Address",
            'required': True,
        })
    )
    education = forms.CharField(
        label='', 
        max_length=256,
        required=False,
        widget=forms.TextInput(attrs={
            'class':'form-control', 
            'name':'education', 
            'placeholder':"Education",
        })
    )
    skills = forms.CharField(
        label='', 
        max_length=256,
        required=False,
        widget=forms.TextInput(attrs={
            'class':'form-control', 
            'name':'skills', 
            'placeholder':"Skills",
        })
    )
    
    def clean_phone(self):
        """
        Validate phone.
        """
        phone = self.cleaned_data.get("phone").strip()
        is_phone = re.compile(r'^\+?1?\d{9,15}$').search(phone)
        if not is_phone:
            raise forms.ValidationError('Enter a valid phone number.')
        return phone


class AddStaffForm(BaseAddStaffStudentForm):
    """
    Add Staff model form.
    """
    recruitment_date = forms.DateField(widget=DateInputWidget(attrs={
            'class': 'form-control float-right',
            'placeholder':'dd/mm/yyyy',
            'required': True,
        })
    )
    class Meta:
        model  = Staff
        fields = ['photo', 'nationality', 'phone', 'address', 'gender', 'birth_date', 'recruitment_date']
        widgets = {'photo':forms.FileInput(
                attrs={'class':'custom-file-input', 'id':'fileInputStaff', 'required': True, } 
        )}

class UpdateStaffAdminForm(AddStaffForm):
    """
    Update Staff Admin model form.
    """
    class Meta:
        model  = Staff
        fields = ['photo', 'nationality', 'phone', 'address', 'gender', 'birth_date', 'recruitment_date']
        widgets = {'photo':forms.FileInput(
                attrs={'class':'custom-file-input', 'id':'fileInputStaff'} 
        )}

class UpdateStaffForm(BaseAddStaffStudentForm):
    """
    Update Staff model form.
    """
    photo = forms.FileField(widget=forms.FileInput(attrs={'class':'custom-file-input', 'id':'fileInputStaff'}))
    
    class Meta:
        model  = Staff
        fields = ['photo', 'nationality', 'phone', 'address', 'gender', 'birth_date', 'education', 'skills']       