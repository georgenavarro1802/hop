from django.shortcuts import render

from app.views import adduserdata


def views(request):
    data = {'title': 'REPORTS'}
    adduserdata(request, data)
    return render(request, 'reports/view.html', data)
