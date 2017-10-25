from django.db import transaction
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from app.forms import WorksForm, NewLeaderForm
from app.functions import (bad_json, MiPaginator, ok_json, convertir_fecha_month_first, CUSTOMER_HOTWIRE_ID,
                           DEFAULT_DISPATCH_ID, USER_GROUP_TECHNICIAN_ID)
from app.models import Works, Customers, Users, Projects, JobTypes
from app.views import adduserdata


def get_number_works_completed_by_weekday_customer(weekday, customerID):
    return Works.objects.filter(is_completed=True, date__week_day=weekday, customer__id=customerID).count()


def views(request):
    data = {'title': 'WORKS'}
    adduserdata(request, data)

    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']

            if action == 'add':
                f = WorksForm(request.POST)
                if f.is_valid():
                    try:
                        with transaction.atomic():

                            if Works.objects.filter(project=f.cleaned_data['project'],
                                                    address=f.cleaned_data['address']).exists():
                                return bad_json(message="Work already exists with that Project and Address. "
                                                        "Please change the project or address and try again. ")

                            project = f.cleaned_data['project']
                            property = f.cleaned_data['property']
                            customer = Customers.objects.get(pk=CUSTOMER_HOTWIRE_ID) if data['is_hotwire'] else f.cleaned_data['customer']
                            address = f.cleaned_data['address']
                            date = convertir_fecha_month_first(f.cleaned_data['date'])
                            initial_time = f.cleaned_data['initial_time']
                            notes = f.cleaned_data['notes']

                            leader = Users.objects.get(pk=DEFAULT_DISPATCH_ID) if data['is_hotwire'] else f.cleaned_data['leader']
                            support1 = f.cleaned_data['support1']
                            support2 = f.cleaned_data['support2']
                            support3 = f.cleaned_data['support3']
                            support4 = f.cleaned_data['support4']
                            support5 = f.cleaned_data['support5']

                            work = Works(project=project,
                                         property=property,
                                         customer=customer,
                                         address=address,
                                         date=date,
                                         initial_time=initial_time,
                                         notes=notes,
                                         leader=leader,
                                         support1=support1,
                                         support2=support2,
                                         support3=support3,
                                         support4=support4,
                                         support5=support5,
                                         created_by=data['myuser'])
                            work.save()

                            return ok_json(data={'redirect_url': '/works',
                                                 'msg': 'You have successfully created a new WORK.'})
                    except Exception as ex:
                        return bad_json(error=1)
                else:
                    return bad_json(message="Form is not valid.")

            if action == 'edit':
                work = Works.objects.get(pk=int(request.POST['id']))
                f = WorksForm(request.POST)
                if f.is_valid():
                    try:
                        with transaction.atomic():

                            if Works.objects.filter(project=f.cleaned_data['project'],
                                                    address=f.cleaned_data['address']).exclude(id=work.id).exists():
                                return bad_json(message="Work already exists with that Project and Address. "
                                                        "Please change the project or address and try again. ")

                            project = f.cleaned_data['project']
                            property = f.cleaned_data['property']
                            customer = Customers.objects.get(pk=CUSTOMER_HOTWIRE_ID) if data['is_hotwire'] else f.cleaned_data['customer']
                            address = f.cleaned_data['address']
                            date = convertir_fecha_month_first(f.cleaned_data['date'])
                            initial_time = f.cleaned_data['initial_time']
                            notes = f.cleaned_data['notes']

                            leader = Users.objects.get(pk=DEFAULT_DISPATCH_ID) if data['is_hotwire'] else f.cleaned_data['leader']
                            support1 = f.cleaned_data['support1']
                            support2 = f.cleaned_data['support2']
                            support3 = f.cleaned_data['support3']
                            support4 = f.cleaned_data['support4']
                            support5 = f.cleaned_data['support5']

                            work.project = project
                            work.property = property
                            work.customer = customer
                            work.address = address
                            work.date = date
                            work.initial_time = initial_time
                            work.notes = notes

                            work.leader = leader
                            work.support1 = support1
                            work.support2 = support2
                            work.support3 = support3
                            work.support4 = support4
                            work.support5 = support5
                            work.save()

                            return ok_json(data={'redirect_url': '/works',
                                                 'msg': 'You have successfully edited the WORK.'})
                    except Exception:
                        return bad_json(error=2)
                else:
                    return bad_json(message="Form is not valid.")

            if action == 'delete':
                work = Works.objects.get(pk=int(request.POST['id']))
                try:
                    with transaction.atomic():
                        if work.workstypes_set.exists():
                            work.workstypes_set.all().delete()
                        work.delete()
                        return ok_json(data={'redirect_url': '/works',
                                             'msg': 'You have successfully deleted the WORK.'})
                except Exception:
                    return bad_json(error=3)

            if action == 'newteam':
                work = Works.objects.get(pk=int(request.POST['id']))
                f = NewLeaderForm(request.POST)
                if f.is_valid():
                    try:
                        with transaction.atomic():

                            work.leader = f.cleaned_data['leader']
                            work.support1 = f.cleaned_data['support1']
                            work.support2 = f.cleaned_data['support2']
                            work.support3 = f.cleaned_data['support3']
                            work.support4 = f.cleaned_data['support4']
                            work.support5 = f.cleaned_data['support5']

                            work.save()
                            return ok_json(data={'redirect_url': '/works',
                                                 'msg': 'You have successfully changed the Team for this work.'})
                    except Exception:
                        return bad_json(error=3)

                else:
                    return bad_json(message='Form is not valid')

            if action == 'get_properties_from_project':
                try:
                    project = Projects.objects.get(pk=int(request.POST['pid']))
                    return ok_json(data={'lista': [(property.id, property.name) for property in project.get_my_properties()]})

                except Exception:
                    return bad_json(error=1)

        return bad_json(error=0)

    else:

        if 'action' in request.GET:
            if 'action' in request.GET:
                action = request.GET['action']

                if action == 'add':
                    try:
                        data['title'] = 'Add Work'
                        form = WorksForm()
                        if data['is_hotwire']:
                            form.for_hotwire()
                        data['form'] = form
                        return render(request, 'works/add.html', data)
                    except Exception:
                        pass

                if action == 'edit':
                    try:
                        data['title'] = 'Edit Work'
                        data['work'] = work = Works.objects.get(pk=request.GET['id'])
                        form = WorksForm(initial={'project': work.project,
                                                  'property': work.property,
                                                  'customer': work.customer,
                                                  'address': work.address,
                                                  'date': work.date.strftime("%m-%d-%Y"),
                                                  'initial_time': work.initial_time,
                                                  'notes': work.notes,
                                                  'leader': work.leader,
                                                  'support1': work.support1,
                                                  'support2': work.support2,
                                                  'support3': work.support3,
                                                  'support4': work.support4,
                                                  'support5': work.support5})
                        if data['is_hotwire']:
                            form.for_hotwire()
                        data['form'] = form
                        return render(request, 'works/edit.html', data)
                    except Exception:
                        pass

                if action == 'delete':
                    try:
                        data['title'] = 'Delete Work'
                        data['work'] = Works.objects.get(pk=request.GET['id'])
                        data['is_delete'] = True
                        return render(request, 'works/delete.html', data)
                    except Exception:
                        pass

                if action == 'details':
                    try:
                        data['title'] = 'Work Details'
                        data['work'] = Works.objects.get(pk=request.GET['id'])
                        return render(request, 'works/details.html', data)
                    except Exception:
                        pass

                if action == 'newteam':
                    try:
                        data['title'] = 'New Team for Work'
                        data['work'] = work = Works.objects.get(pk=request.GET['id'])
                        data['form'] = NewLeaderForm(initial={'leader': work.leader,
                                                              'support1': work.support1,
                                                              'support2': work.support2,
                                                              'support3': work.support3,
                                                              'support4': work.support4,
                                                              'support5': work.support5})
                        return render(request, 'works/newteam.html', data)
                    except Exception:
                        pass

                if action == 'customer_reports':
                    data['title'] = 'Reports and Charts - HOTWIRE'
                    data['report1_title'] = 'Job Types - Completed Works - HOTWIRE'
                    data['report2_title'] = 'Top 5 HOP Technicians - HOTWIRE'
                    data['report3_title'] = 'Complete Works by Weekdays - HOTWIRE'
                    data['jobtypes'] = JobTypes.objects.filter(workstypes__work__is_completed=True,
                                                               workstypes__isnull=False,
                                                               workstypes__work__customer__id=CUSTOMER_HOTWIRE_ID).distinct()

                    user_list = []
                    for u in Users.objects.filter(group=USER_GROUP_TECHNICIAN_ID, leader__is_completed=True).distinct():
                        user_list.append((u.get_number_works_completed(),
                                          u.average_rating_works_completed(),
                                          u.user.username))

                    data['user_list'] = sorted(user_list, reverse=True)[:5]

                    weekdays_works = []
                    # Weeks days in Django -> 1(Sunday) to 7(Saturday)
                    for i in range(2, 7):
                        weekdays_works.append(get_number_works_completed_by_weekday_customer(i, CUSTOMER_HOTWIRE_ID))

                    data['weekdays_works'] = weekdays_works
                    return render(request, 'reports/customer_reports.html', data)

            return HttpResponseRedirect('/works')

        else:

            works = Works.objects.order_by('-created_at')

            if 'h' in request.GET and request.GET['h'] != '':
                works = works.filter(customer__id=CUSTOMER_HOTWIRE_ID)

            search = None
            if 's' in request.GET and request.GET['s'] != '':
                search = request.GET['s']

            if search:
                works = works.filter(Q(address__icontains=search) | Q(id__icontains=search))

            paging = MiPaginator(works, 20)

            p = 1
            if 'page' in request.GET:
                p = int(request.GET['page'])
            page = paging.page(p)

            data['paging'] = paging
            data['ranges_paging'] = paging.pages_range(p)
            data['page'] = page
            data['works'] = page.object_list
            data['search'] = search if search else ''

            return render(request, 'works/view.html', data)
