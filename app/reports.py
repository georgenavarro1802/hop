from django.http import HttpResponseRedirect
from django.shortcuts import render

from app.functions import (EVALUATION_TYPE_BAD, EVALUATION_TYPE_REGULAR, EVALUATION_TYPE_GOOD,
                           EVALUATION_TYPE_VERY_GOOD,  EVALUATION_TYPE_EXCELLENT)
from app.models import Works, JobTypes
from app.views import adduserdata


def views(request):
    data = {'title': 'REPORTS'}
    adduserdata(request, data)

    if 'action' in request.GET:
        action = request.GET['action']

        data['works'] = works = Works.objects.all()

        if action == 'complete_incomplete_works':
            data['report_title'] = 'Complete and Incomplete Works'
            data['complete_works'] = works.filter(is_completed=True).count()
            data['incomplete_works'] = works.filter(is_completed=False).count()
            return render(request, 'reports/completed_works.html', data)

        if action == 'evaluation_works':
            data['report_title'] = 'Evaluation of Completed Works'
            complete_works = works.filter(is_completed=True)
            data['evaluations_bad'] = complete_works.filter(evaluation=EVALUATION_TYPE_BAD).count()
            data['evaluations_regular'] = complete_works.filter(evaluation=EVALUATION_TYPE_REGULAR).count()
            data['evaluations_good'] = complete_works.filter(evaluation=EVALUATION_TYPE_GOOD).count()
            data['evaluations_very_good'] = complete_works.filter(evaluation=EVALUATION_TYPE_VERY_GOOD).count()
            data['evaluations_excellent'] = complete_works.filter(evaluation=EVALUATION_TYPE_EXCELLENT).count()
            return render(request, 'reports/evaluation_works.html', data)

        if action == 'jobtypes_works':
            data['report_title'] = 'Job Types in Completed Works'
            data['jobtypes'] = JobTypes.objects.filter(workstypes__work__is_completed=True,
                                                       workstypes__isnull=False).distinct()
            return render(request, 'reports/jobtypes_works.html', data)

        if action == 'workers_perfomances':
            data['report_title'] = 'Workers Perfomances'
            return render(request, 'reports/workers_perfomances.html', data)

        if action == 'workers_track':
            data['report_title'] = 'Workers Tracks'
            return render(request, 'reports/workers_track.html', data)

    return HttpResponseRedirect('/')
