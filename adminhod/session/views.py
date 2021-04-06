import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string

from student.models import SessionYear
from adminhod.utils import search, paginate 
from .forms import AddSessionForm

def add_session(request):
    """
    Add session year.
    """
    if request.method == 'POST':
        session_form = AddSessionForm(request.POST)
        if session_form.is_valid():
            # get submitted date range and split it to valid start and end date.
            date_range_str = request.POST.get('date_range')
            start_date = datetime.datetime.strptime(date_range_str[:10], '%m/%d/%Y').date()
            end_date = datetime.datetime.strptime(date_range_str[13:], '%m/%d/%Y').date()
            # create new session.
            SessionYear.objects.create(start_date=start_date, end_date=end_date)
            # Display success message.
            messages.success(request, f'New session has been added successfully.', extra_tags='add-session')
            # if save and add another.
            if 'save_and_add_another' in request.POST:
                # redirect to add sessions url.
                return redirect('adminhod:add-session')
            # if save.
            elif 'save' in request.POST:
                # redirect to manage sessions url.
                return redirect('adminhod:manage-session')
    else:
        session_form = AddSessionForm()
    context = {'form':session_form}
    return render(request, 'session/add_session.html', context)    

def validate_session_view(request):
    """
    Validate session asynchronously by ajax, and check if it's already been taken or not, in case of adding new session.
    """
    # get submitted session.
    date_range_str = request.GET.get('session')
    # check if an account with this session already exists, in case of adding new session.
    is_session_taken = SessionYear.objects.filter(date_range__iexact=date_range_str).exists()    
    data = {'is_session_taken':is_session_taken}
    if data['is_session_taken']:
        data['error_message'] = 'This Session already exists.'
    return JsonResponse(data)

def validate_session_update_view(request, session_id):
    """
    Validate session asynchronously by ajax, and check if it's already been taken or not, in case of updating session.
    """
    session = get_object_or_404(SessionYear, pk=session_id)
    # get submitted session.
    date_range_str = request.GET.get('session', None)
    # check if an account with this session already exists, in case of updating existing session.
    is_session_taken = SessionYear.objects.filter(date_range__iexact=date_range_str).exclude(date_range__iexact=session.date_range).exists()    
    data = {'is_session_taken':is_session_taken}
    if data['is_session_taken']:
        data['error_message'] = 'This session already exists.'
    return JsonResponse(data)

def manage_session(request):
    """
    Display all session years.
    Search sessions by start or end date, ordered by start date.
    """
    # get all session years.
    sessions_qs = SessionYear.objects.all()
    # paginate the sessions list.
    page_obj_sessions = paginate(sessions_qs)
    if request.is_ajax():
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        data = dict()  
        # filter sessions by start or end date, ordered by start date.
        sessions = search(q, session_qs=sessions_qs)
        # paginate the sessions list.
        page_obj_sessions = paginate(sessions)    
        context = {'sessions': page_obj_sessions, 'request':request}
        data['html_session_list'] = render_to_string('session/includes/partial_session_list.html', context)
        data['html_session_pagination'] = render_to_string('session/includes/partial_session_pagination.html', context)
        return JsonResponse(data)
    context = {'sessions': page_obj_sessions}
    return render(request, 'session/manage_session.html', context)

def paginate_session(request):
    """
    Paginate all session years.
    """
    # get all session years.
    sessions_qs = SessionYear.objects.all()
    # get page number of paginator.
    page_number = request.GET.get('page').split('&')[0]
    data = dict()
    # paginate the search results.
    if request.GET.get('search'):
        # get entered value in search input field.
        q = request.GET.get('search').strip()
        # filter sessions by start or end date, ordered by start date.
        sessions = search(q, session_qs=sessions_qs)
        # paginate the sessions list.
        page_obj_sessions = paginate(sessions, page_number)
    else:
        # paginate the sessions list.
        page_obj_sessions = paginate(sessions_qs, page_number)    
    context = {'sessions':page_obj_sessions, 'request':request}
    data['html_session_list'] = render_to_string('session/includes/partial_session_list.html', context)
    data['html_session_pagination'] = render_to_string('session/includes/partial_session_pagination.html', context)    
    return JsonResponse(data)

def update_session(request, session_id):
    """
    Take session's id, and get this session by its id.
    Update this session.
    """
    # get session year by its id.
    session = get_object_or_404(SessionYear, pk=session_id)
    data = dict()
    if request.method == 'POST':
        session_form = AddSessionForm(request.POST, instance=session)
        if session_form.is_valid():
            date_range_str = request.POST.get('date_range')
            # update session.
            session.date_range = date_range_str
            session.start_date = datetime.datetime.strptime(date_range_str[:10], '%m/%d/%Y').date()
            session.end_date = datetime.datetime.strptime(date_range_str[13:], '%m/%d/%Y').date()
            session.save()
            data['form_is_valid'] = True 
            data['is_update'] = True
            sessions = SessionYear.objects.all()
            data['html_session_list'] = render_to_string('session/includes/partial_session_list.html', {'sessions': sessions})
        else:
            data['form_is_valid'] = False   
    else:
        session_form = AddSessionForm(instance=session)
        context = {'form': session_form}
        data['html_form'] = render_to_string('session/includes/partial_session_update.html', context, request=request)
    return JsonResponse(data)     

def delete_session(request, session_id):
    """
    Take session's id, and get this session by its id.
    Delete this session.
    """
    # get session year by its id.
    session = get_object_or_404(SessionYear, pk=session_id)
    data = dict()
    if request.method == 'POST':
        # delete session.
        session.delete()
        data['form_is_valid'] = True 
        data['is_update'] = False 
        # get all session years.
        sessions = SessionYear.objects.all()
        data['html_session_list'] = render_to_string('session/includes/partial_session_list.html', {'sessions': sessions})
    else:
        context = {'session': session}
        data['html_form'] = render_to_string('session/includes/partial_session_delete.html', context, request=request)
    return JsonResponse(data)    
