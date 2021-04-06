import datetime

from django import template

register = template.Library()

@register.simple_tag
def is_deadline_exceeded(deadline, allow_submission_after_deadline):
    """
    Take value of deadline date, and boolean value of if it's allowed to submit assignments after deadline.
    """
    # if it's not allowed to submit assignments after deadline.
    if not allow_submission_after_deadline:
        # check if today's date already exceeded the deadline or not.  
        return datetime.datetime.now().date() > deadline
    # if allowed.
    else:
        return False    
