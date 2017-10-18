from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from app.forms import JobTypesForm
from app.functions import bad_json, MiPaginator, ok_json
from app.models import JobTypes
from app.views import adduserdata


def views(request):
    data = {'title': 'JOB TYPES'}
    adduserdata(request, data)

    if data['is_hotwire'] or data['is_dispatch']:
        return HttpResponseRedirect('/works')

    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']

            if action == 'add':
                f = JobTypesForm(request.POST)
                if f.is_valid():
                    try:
                        with transaction.atomic():

                            if JobTypes.objects.filter(name=f.cleaned_data['name']).exists():
                                return bad_json(message="Job Type already exists. "
                                                        "Please change the name of the job type and try again. ")
                            jobtype = JobTypes(name=f.cleaned_data['name'])
                            jobtype.save()
                            return ok_json(data={'redirect_url': '/jobtypes',
                                                 'msg': 'You have successfully created a new JOB TYPE.'})
                    except Exception:
                        return bad_json(error=1)
                else:
                    return bad_json(message="Form is not valid.")

            if action == 'edit':
                jobtype = JobTypes.objects.get(pk=int(request.POST['id']))
                f = JobTypesForm(request.POST)
                if f.is_valid():
                    try:
                        with transaction.atomic():

                            if JobTypes.objects.filter(name=f.cleaned_data['name']).exclude(id=jobtype.id).exists():
                                return bad_json(message="Job Type already exists. "
                                                        "Please change the name of the job type and try again. ")
                            jobtype.name = f.cleaned_data['name']
                            jobtype.save()
                            return ok_json(data={'redirect_url': '/jobtypes',
                                                 'msg': 'You have successfully edited the JOB TYPE.'})
                    except Exception:
                        return bad_json(error=2)
                else:
                    return bad_json(message="Form is not valid.")

            if action == 'delete':
                jobtype = JobTypes.objects.get(pk=int(request.POST['id']))
                try:
                    with transaction.atomic():
                        jobtype.delete()
                        return ok_json(data={'redirect_url': '/jobtypes',
                                             'msg': 'You have successfully deleted the JOB TYPE.'})
                except Exception:
                    return bad_json(error=3)

        return bad_json(error=0)

    else:

        if 'action' in request.GET:
            if 'action' in request.GET:
                action = request.GET['action']

                if action == 'add':
                    try:
                        data['title'] = 'New Job Type'
                        data['form'] = JobTypesForm()
                        return render(request, 'jobtypes/add.html', data)
                    except Exception:
                        pass

                if action == 'edit':
                    try:
                        data['title'] = 'Edit Job Type'
                        data['jobtype'] = jobtype = JobTypes.objects.get(pk=request.GET['id'])
                        data['form'] = JobTypesForm(initial={'name': jobtype.name})
                        return render(request, 'jobtypes/edit.html', data)
                    except Exception:
                        pass

                if action == 'delete':
                    try:
                        data['title'] = 'Delete Job Type'
                        data['jobtype'] = JobTypes.objects.get(pk=request.GET['id'])
                        data['is_delete'] = True
                        return render(request, 'jobtypes/delete.html', data)
                    except Exception:
                        pass

            return HttpResponseRedirect('/jobtypes')

        else:

            job_types = JobTypes.objects.order_by('name')

            search = None
            if 's' in request.GET and request.GET['s'] != '':
                search = request.GET['s']

            if search:
                job_types = job_types.filter(name__icontains=search).order_by('name')

            paging = MiPaginator(job_types, 25)

            p = 1
            if 'page' in request.GET:
                p = int(request.GET['page'])
            page = paging.page(p)

            data['paging'] = paging
            data['ranges_paging'] = paging.pages_range(p)
            data['page'] = page
            data['jobtypes'] = page.object_list
            data['search'] = search if search else ''
            return render(request, 'jobtypes/view.html', data)
