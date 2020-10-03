import re

from django.shortcuts import render
from ratelimit.core import is_ratelimited
from ratelimit.decorators import ratelimit
from webpreview import web_preview

from web.models import Content


def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None


def home(request):
    cntnt = Content.objects.all().order_by('-created_at')
    return render(request, 'web/index.html', {"content": cntnt})


@ratelimit(key='ip', rate='1/m')
def share(request):
    if request.method == 'GET':
        return render(request, 'web/share.html')
    if request.method == 'POST':
        was_limited = getattr(request, 'limited', False)
        print(was_limited)
        if was_limited:
            return render(request, 'web/share.html', {"error": "Please don't spam, you can share one URL every minute. Thanks!"})

        url = request.POST.get('url')
        if not is_valid_url(url):
            return render(request, 'web/share.html', {"error": "Not a valid URL!"})
        title, desc, img_url = web_preview(url)
        if title and img_url:
            cntnt = Content(
                link=url,
                title=title,
                description=desc,
                image=img_url,

            )
            cntnt.save()
            return render(request, 'web/share.html', {"success": "URL added successfully"})

        return render(request, 'web/share.html', {"error": "URL cannot be parsed, please try another URL."})
