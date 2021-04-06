from django import template

register = template.Library()

@register.simple_tag
def relative_url(value, urlencode=None):
    """
    Return the URL-encoded querystring for the current page
    updating the params with the key/value pairs passed to the tag.
    
    E.g: given the value=1 , field_name='page' , urlencode='http://127.0.0.1:8000/?page=1&filter=&title='
    {% relative_url 1 'page' request.GET.urlencode %} outputs ?page=1&filter=&title=

    """
    url = '{}'.format(value)    #?page=1
    if urlencode:
        querystring = urlencode.split('&')  #['http://127.0.0.1:8000/jobs/favourite/?page=1', 'filter=5', 'title=8',]
        # filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)  #['filter=5', 'title=8',]
        filtered_querystring = querystring[1:]
        encoded_querystring = '&'.join(filtered_querystring) #filter=&title=
        url = '{}&{}'.format(url, encoded_querystring)   #?page=1&filter=&title=
    return url 
