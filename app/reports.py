from django.http import HttpResponseRedirect
from django.shortcuts import render

from app.views import adduserdata


def views(request):
    data = {'title': 'REPORTS'}
    adduserdata(request, data)

    if 'action' in request.GET:
        action = request.GET['action']

        if action == 'complete_works':
            data['report_title'] = 'Complete Works'
            return render(request, 'reports/completed_works.html', data)

        if action == 'incomplete_works':
            data['report_title'] = 'Incomplete Works'
            return render(request, 'reports/incompleted_works.html', data)

        if action == 'evaluation_works':
            data['report_title'] = 'Evaluation Works'
            return render(request, 'reports/evaluation_works.html', data)

        if action == 'jobtypes_works':
            data['report_title'] = 'Job Types'
            return render(request, 'reports/jobtypes_works.html', data)

    return HttpResponseRedirect('/')
