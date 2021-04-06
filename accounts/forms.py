from django import forms
# from django.contrib.auth import password_validation
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm


User = get_user_model()

class UserAddForm(forms.ModelForm):
    """
    User creation form class.
    """
    full_name = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={'class':'form-control', 'name':'fullname', 'placeholder':"Full Name"}),
    )
    email = forms.EmailField(
        label='', 
        widget=forms.EmailInput(attrs={'class':'form-control js-validate-email', 'name':'email', 'placeholder':"Email"}),
    )
    email2 = forms.EmailField(
        label='', 
        widget=forms.EmailInput(attrs={'class':'form-control', 'name':'confirm_email', 'placeholder':"Confirm Email"}),
    )
    
    class Meta:
        model   = User
        fields  = ['full_name', 'email', 'email2']    

    def clean_email2(self):
        """
        Validate email 2.
        """
        email1 = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get('email2') 
        # check if the two emails match.
        if email1 != email2:
            raise forms.ValidationError('The two email fields didn’t match.')
        # check if the email has already been used.  
        if User.objects.filter(email__iexact=email2).exists():
            raise forms.ValidationError("An account with this Email already exists.")
        return email2

class UpdateUserForm(forms.ModelForm):
    """
    Update User model form.
    """
    full_name = forms.CharField(
        label='Full name', 
        widget=forms.TextInput(attrs={'class':'form-control', 'name':'full_name'}),
    )
    email = forms.EmailField(
        label='Email address', 
        widget=forms.EmailInput(attrs={'class':'form-control js-validate-email-update', 'name':'email'}),
    )

    class Meta:
        model  = User
        fields = ['full_name', 'email']

    def __init__(self, *args, **kwargs):
        self.staff_student = kwargs.pop("staff_student", None)
        super(UpdateUserForm, self).__init__(*args, **kwargs)    

    def clean_email(self):
        """
        Validate email.
        """
        email = self.cleaned_data.get("email")
        # check if the email has already been used.   
        if User.objects.filter(email__iexact=email).exclude(email__iexact=self.staff_student.user.email).exists():
            raise forms.ValidationError("An account with this Email already exists.")
        return email

class EmailValidationOnForgotPassword(PasswordResetForm):
    """
    Override password reset form email field and its validation.
    """
    email = forms.EmailField(
        label='',
        max_length=255,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class':'form-control', 'name':'email', 'placeholder':"Email", 'required':True})
    )

    def clean_email(self):
        """
        Validate email.
        """
        # fetch entered email.
        email = self.cleaned_data['email']
        # check if the entered email doesn't exist.
        if not User.objects.filter(email__iexact=email, active=True).exists():
            raise forms.ValidationError("Your email was entered incorrectly. Please enter it again.")
        return email

class PasswordFieldsOnForgotPassword(SetPasswordForm):
    """
    Override set password form password fields.
    """
    new_password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control mb-2', 'placeholder':"New Password"}),
        strip=False,
        # help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control', 'placeholder':"Confirm Password"}),
    )

class PasswordFieldsOnChangePassword(PasswordChangeForm):
    """
    Override password change form password fields.
    """
    old_password = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True, 'class':'form-control mb-2', 'placeholder':"Old Password"}),
    )
    new_password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control mb-2', 'placeholder':"New Password"}),
        strip=False,
        # help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control', 'placeholder':"Confirm Password"}),
    )
