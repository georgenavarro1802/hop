from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from app.forms import ProjectsForm, PropertiesForm
from app.functions import bad_json, MiPaginator, ok_json
from app.models import Projects, Properties
from app.views import adduserdata


def views(request):
    data = {'title': 'PROPERTIES'}
    adduserdata(request, data)

    if data['is_dispatch']:
        return HttpResponseRedirect('/works')

    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']

            if action == 'add':
                f = PropertiesForm(request.POST)
                if f.is_valid():
                    try:
                        with transaction.atomic():

                            if Properties.objects.filter(project=f.cleaned_data['project'],
                                                         name=f.cleaned_data['name']).exists():
                                return bad_json(message="Property already exists. "
                                                        "Please change the name and the project and try again. ")

                            property = Properties(project=f.cleaned_data['project'],
                                                  name=f.cleaned_data['name'])
                            property.save()
                            return ok_json(data={'redirect_url': '/properties',
                                                 'msg': 'You have successfully created a new PROPERTY.'})
                    except Exception:
                        return bad_json(error=1)
                else:
                    return bad_json(message="Form is not valid.")

            if action == 'edit':
                property = Properties.objects.get(pk=int(request.POST['id']))
                f = PropertiesForm(request.POST)
                if f.is_valid():
                    try:
                        with transaction.atomic():

                            if Properties.objects.filter(project=f.cleaned_data['project'],
                                                         name=f.cleaned_data['name']).exclude(id=property.id).exists():
                                return bad_json(message="Property already exists. "
                                                        "Please change the name and the project and try again. ")

                            property.project = f.cleaned_data['project']
                            property.name = f.cleaned_data['name']
                            property.save()
                            return ok_json(data={'redirect_url': '/properties',
                                                 'msg': 'You have successfully edited the PROPERTY.'})
                    except Exception as ex:
                        return bad_json(error=2)
                else:
                    return bad_json(message="Form is not valid.")

            if action == 'delete':
                property = Properties.objects.get(pk=int(request.POST['id']))
                try:
                    with transaction.atomic():
                        if property.works_set.exists():
                            property.works_set.all().delete()
                        property.delete()
                        return ok_json(data={'redirect_url': '/properties',
                                             'msg': 'You have successfully deleted the PROJECT.'})
                except Exception:
                    return bad_json(error=3)

        return bad_json(error=0)

    else:

        if 'action' in request.GET:
            if 'action' in request.GET:
                action = request.GET['action']

                if action == 'add':
                    try:
                        data['title'] = 'New Property'
                        data['form'] = PropertiesForm()
                        return render(request, 'properties/add.html', data)
                    except Exception:
                        pass

                if action == 'edit':
                    try:
                        data['title'] = 'Edit Property'
                        data['property'] = property = Properties.objects.get(pk=request.GET['id'])
                        data['form'] = PropertiesForm(initial={'name': property.name,
                                                               'project': property.project})
                        return render(request, 'properties/edit.html', data)
                    except Exception:
                        pass

                if action == 'delete':
                    try:
                        data['title'] = 'Delete Property'
                        data['property'] = Properties.objects.get(pk=request.GET['id'])
                        data['is_delete'] = True
                        return render(request, 'properties/delete.html', data)
                    except Exception:
                        pass

            return HttpResponseRedirect('/properties')

        else:

            properties = Properties.objects.order_by('-created_at')

            search = None
            if 's' in request.GET and request.GET['s'] != '':
                search = request.GET['s']

            if search:
                properties = properties.filter(name__icontains=search)

            paging = MiPaginator(properties, 20)

            p = 1
            if 'page' in request.GET:
                p = int(request.GET['page'])
            page = paging.page(p)

            data['paging'] = paging
            data['ranges_paging'] = paging.pages_range(p)
            data['page'] = page
            data['properties'] = page.object_list

            return render(request, 'properties/view.html', data)
