from django.shortcuts import render


def error_404(request, exception):
    if len(str(exception)) > 50:
        exception = ''
    return render(request, 'errors/404.html', {'message': exception})
