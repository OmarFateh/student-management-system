from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.views import PasswordResetConfirmView

from .forms import PasswordFieldsOnChangePassword, PasswordFieldsOnForgotPassword
from .decorators import unauthenticated_user

User = get_user_model()
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'

# Restrict the authenticated user from visiting this page and redirect to home page.
@unauthenticated_user
def user_login_view(request):
    """
    Take request and login user.
    """
    if request.method == "POST":
        # fetch submitted data.
        email = request.POST.get("email")
        password = request.POST.get("password")
        # check if the entered email exists.
        user = authenticate(username=email, password=password)
        # Email and Password are correct. 
        if user:
            # login user.
            login(request, user)
            if user.user_type == 'HOD':
                return redirect('adminhod:dashboard')
            elif user.user_type == 'STAFF':   
                return redirect('staff:dashboard')    
            elif user.user_type == 'STUDENT':    
                return redirect('student:dashboard')      
        # Email or Password doesn't exist. 
        else:
            # Display error message.
            messages.error(request, 'Email or Passowrd is incorrect.', extra_tags='login')
    return render(request, 'accounts/login.html', {})

def validate_email_view(request):
    """
    Validate email asynchronously by ajax, and check if it's already been taken or not, in case of registering new user.
    """
    # get submitted email.
    email = request.GET.get('email', None)
    try:
        # check if an account with this email already exists, in case of updating user's profile.
        is_email_taken = User.objects.filter(email__iexact=email).exclude(email__iexact=request.user.email).exists()
    except:    
        # check if an account with this email already exists, in case of registering new user.
        is_email_taken = User.objects.filter(email__iexact=email).exists()   
    data = {'is_email_taken':is_email_taken}
    if data['is_email_taken']:
        data['error_message'] = 'An account with this Email already exists.'
    return JsonResponse(data)

def validate_email_update_view(request, user_id):
    """
    Validate email asynchronously by ajax, and check if it's already been taken or not, in case of updating user's profile.
    """
    user = get_object_or_404(User, pk=user_id)
    # get submitted email.
    email = request.GET.get('email', None)
    # check if an account with this email already exists, in case of updating user's profile.
    is_email_taken = User.objects.filter(email__iexact=email).exclude(email__iexact=user.email).exists()    
    data = {'is_email_taken':is_email_taken}
    if data['is_email_taken']:
        data['error_message'] = 'An account with this Email already exists.'
    return JsonResponse(data)

def user_logout_view(request):
    """
    Take request and logout user.
    """
    logout(request)
    return redirect('accounts:login') 

def change_password(request):
    """
    Change user's password.
    """
    user_obj = request.user
    if request.method == 'POST':
        form = PasswordFieldsOnChangePassword(user_obj, request.POST)
        if form.is_valid():
            user = form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one.
            update_session_auth_hash(request, user)  # Important!
            user_obj.previously_logged_in = True
            user_obj.save()
            return redirect('accounts:password-change-done')
    else:
        form = PasswordFieldsOnChangePassword(user_obj)
    return render(request, 'accounts/password_change_form.html', {'form': form})

def change_password_done(request):
    """
    Change password done.
    """
    return render(request, 'accounts/password_change_done.html', {})


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Custom password reset confirmation.
    """
    template_name = 'accounts/password_reset_form.html'
    form_class = PasswordFieldsOnForgotPassword

    def form_valid(self, form):
        """
        Take form, and validate it.
        """
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        # update previously logged in field to True.
        user_obj = self.request.user
        user_obj.previously_logged_in = True
        user_obj.save()
        if self.post_reset_login:
            login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)