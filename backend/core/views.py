from django.conf import settings
from django.shortcuts import render

from services.utils.time_functions import get_datetime_today


def page_not_found(request, exception):
    template = 'core/404.html'
    return render(request, template, status=404)


def server_error(request):
    template = 'core/500.html'
    return render(request, template, status=500)


def permission_denied(request, exception):
    template = 'core/403.html'
    return render(request, template, status=403)


def csrf_failure(request):
    template = 'core/403csrf.html'
    return render(request, template)


def log_view(request):
    template = 'core/log.html'
    with open(settings.LOG_FILE_NAME, 'r') as file:
        context = {
            'title': f'Лог {get_datetime_today()}',
            'log': file.read()
        }
    return render(request, template, context)
