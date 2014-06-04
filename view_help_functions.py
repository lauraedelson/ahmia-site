""" Generig help functions for the views. """
from django.template import Context, loader
from django.http import HttpResponse
from ahmia.models import HiddenWebsiteDescription, HiddenWebsite
from django.core.exceptions import ValidationError
import re # Regular expressions

def validate_onion_url(url):
    """ Test is url correct onion URL."""
    #Must be like http://3g2upl4pq6kufc4m.onion/
    if len(url) != 30:
        raise ValidationError(u'%s length is not 30' % url)
    if url[0:7] != 'http://':
        raise ValidationError(u'%s is not beginning with http://' % url)
    if url[-7:] != '.onion/':
        raise ValidationError(u'%s is not ending with .onion/' % url)
    if not re.match("[a-z2-7]{16}", url[7:-7]):
        raise ValidationError(u'%s is not valid onion domain' % url)

def render_page(page):
    """ Return a page without any parameters """
    onions = HiddenWebsite.objects.all()
    template = loader.get_template(page)
    desc = HiddenWebsiteDescription.objects.order_by('about', '-updated')
    desc = desc.distinct('about')
    content = Context({'description_list': desc,
        'count_banned': onions.filter(banned=True).count(),
        'count_online': onions.filter(banned=False, online=True).count()})
    return HttpResponse(template.render(content))

def get_client_ip(request):
    """Returns the IP address of the HTTP request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_addr = x_forwarded_for.split(',')[0]
    else:
        ip_addr = request.META.get('REMOTE_ADDR')
    return ip_addr

def redirect_page(message, time, url):
    """Build and return redirect page."""
    template = loader.get_template('redirect.html')
    content = Context({'message': message,
    'time': time,
    'redirect': url})
    return HttpResponse(template.render(content))

def round_to_next_multiple_of(number, divisor):
    """
    Return the lowest x such that x is at least the number
    and x modulo divisor == 0
    """
    number = number + divisor - 1
    number = number - number % divisor
    return number
