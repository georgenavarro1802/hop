from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from app.forms import ProjectsForm
from app.functions import bad_json, MiPaginator, ok_json
from app.models import Projects
from app.views import adduserdata


def views(request):
    data = {'title': 'PROJECTS'}
    adduserdata(request, data)

    if data['is_hotwire'] or data['is_dispatch']:
        return HttpResponseRedirect('/works')

    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']

            if action == 'add':
                f = ProjectsForm(request.POST)
                if f.is_valid():
                    try:
                        with transaction.atomic():

                            if Projects.objects.filter(name=f.cleaned_data['name']).exists():
                                return bad_json(message="Project already exists. "
                                                        "Please change the name of the project and try again. ")
                            project = Projects(name=f.cleaned_data['name'],
                                               grupo=f.cleaned_data['grupo'])
                            project.save()
                            return ok_json(data={'redirect_url': '/projects',
                                                 'msg': 'You have successfully created a new PROJECT.'})
                    except Exception:
                        return bad_json(error=1)
                else:
                    return bad_json(message="Form is not valid.")

            if action == 'edit':
                project = Projects.objects.get(pk=int(request.POST['id']))
                f = ProjectsForm(request.POST)
                if f.is_valid():
                    try:
                        with transaction.atomic():

                            if Projects.objects.filter(name=f.cleaned_data['name']).exclude(id=project.id).exists():
                                return bad_json(message="Project already exists. "
                                                        "Please change the name of the project and try again. ")
                            project.name = f.cleaned_data['name']
                            project.grupo = f.cleaned_data['grupo']
                            project.save()
                            return ok_json(data={'redirect_url': '/projects',
                                                 'msg': 'You have successfully edited the PROJECT.'})
                    except Exception:
                        return bad_json(error=2)
                else:
                    return bad_json(message="Form is not valid.")

            if action == 'delete':
                project = Projects.objects.get(pk=int(request.POST['id']))
                try:
                    with transaction.atomic():
                        if project.works_set.exists():
                            project.works_set.all().delete()
                        project.delete()
                        return ok_json(data={'redirect_url': '/projects',
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
                        data['title'] = 'New Project'
                        data['form'] = ProjectsForm()
                        return render(request, 'projects/add.html', data)
                    except Exception:
                        pass

                if action == 'edit':
                    try:
                        data['title'] = 'Edit Project'
                        data['project'] = project = Projects.objects.get(pk=request.GET['id'])
                        data['form'] = ProjectsForm(initial={'name': project.name,
                                                             'grupo': project.grupo})
                        return render(request, 'projects/edit.html', data)
                    except Exception:
                        pass

                if action == 'delete':
                    try:
                        data['title'] = 'Delete Project'
                        data['project'] = Projects.objects.get(pk=request.GET['id'])
                        data['is_delete'] = True
                        return render(request, 'projects/delete.html', data)
                    except Exception:
                        pass

            return HttpResponseRedirect('/projects')

        else:

            projects = Projects.objects.order_by('-created_at')

            search = None
            if 's' in request.GET and request.GET['s'] != '':
                search = request.GET['s']

            if search:
                projects = projects.filter(name__icontains=search)

            paging = MiPaginator(projects, 10)

            p = 1
            if 'page' in request.GET:
                p = int(request.GET['page'])
            page = paging.page(p)

            data['paging'] = paging
            data['ranges_paging'] = paging.pages_range(p)
            data['page'] = page
            data['projects'] = page.object_list

            return render(request, 'projects/view.html', data)
