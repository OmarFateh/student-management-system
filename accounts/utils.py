import random
import string

from django.contrib.auth import get_user_model


def random_string_generator(length=10):
    """
    Generate a random alphanumeric string of letters and digits of a given fixed length.
    """
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

def unique_password_generator(new_password=None):
    """
    Generate a unique password of given instance.
    """
    # check if the given arguments have a value of new password.
    # if yes, assign the given value to the password field. 
    if new_password is not None:
        password = new_password
    # if not, generate a password of a random string.
    else:
        password = random_string_generator()
    # get the instance class. 
    User = get_user_model()
    # check if there's any item with the same password.
    qs_exists = User.objects.filter(password=password).exists()
    # if yes, generate a new password of a random string and return recursive function with the new password.
    if qs_exists:
        new_password = random_string_generator()
        return unique_password_generator(new_password=new_password)
    return password
