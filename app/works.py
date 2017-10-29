from django.db import transaction
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from app.forms import WorksForm, NewLeaderForm
from app.functions import (bad_json, MiPaginator, ok_json, convertir_fecha_month_first, CUSTOMER_HOTWIRE_ID,
                           DEFAULT_DISPATCH_ID, USER_GROUP_TECHNICIAN_ID, USER_ADMIN_DEVELOPERS_IDS,
                           USER_GROUP_HOTWIRE_ID, CUSTOMER_CREATE_NEW_CUSTOMER_ID, PROJECT_GROUP_HOTWIRE)
from app.models import Works, Customers, Users, Projects, JobTypes, Properties
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

                            customer = f.cleaned_data['customer']

                            if not customer:
                                return bad_json(message='Please select one of the Customers options menu')

                            new_customer = None
                            if customer.id == CUSTOMER_CREATE_NEW_CUSTOMER_ID:      # New customer
                                customer_name = f.cleaned_data['customer_name']
                                customer_email = f.cleaned_data['customer_email']
                                customer_phone = f.cleaned_data['customer_phone']

                                new_customer = Customers(name=customer_name,
                                                         email=customer_email,
                                                         phone=customer_phone,
                                                         is_company=False)
                                new_customer.save()

                            if new_customer:
                                customer = new_customer

                            # Work details
                            project = f.cleaned_data['project']
                            property = f.cleaned_data['property']
                            address = f.cleaned_data['address']
                            date = convertir_fecha_month_first(f.cleaned_data['date'])
                            initial_time = f.cleaned_data['initial_time']
                            notes = f.cleaned_data['notes']

                            # Work Team
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

            works = Works.objects.order_by('-date')

            if 'h' in request.GET and request.GET['h'] != '':
                works = works.filter(Q(customer__id=CUSTOMER_HOTWIRE_ID) |
                                     Q(created_by__group=USER_GROUP_HOTWIRE_ID) |
                                     Q(project__grupo=PROJECT_GROUP_HOTWIRE)).distinct()

            # Filters
            project_id = None
            if 'project' in request.GET and int(request.GET['project']) > 0:
                project_id = int(request.GET['project'])

            property_id = None
            if 'property' in request.GET and int(request.GET['property']) > 0:
                property_id = int(request.GET['property'])

            jobtype_id = None
            if 'jobtype' in request.GET and int(request.GET['jobtype']) > 0:
                jobtype_id = int(request.GET['jobtype'])

            team_id = None
            if 'team' in request.GET and int(request.GET['team']) > 0:
                team_id = int(request.GET['team'])

            status_id = None
            if 'status' in request.GET and int(request.GET['status']) > 0:
                status_id = int(request.GET['status'])

            creator_id = None
            if 'creator' in request.GET and int(request.GET['creator']) > 0:
                creator_id = int(request.GET['creator'])

            initial_date = None
            if 'idate' in request.GET and request.GET['idate']:
                initial_date = convertir_fecha_month_first(request.GET['idate'])

            end_date = None
            if 'edate' in request.GET and request.GET['edate']:
                end_date = convertir_fecha_month_first(request.GET['edate'])

            code = ''
            if 'code' in request.GET and request.GET['code'] != '':
                code = request.GET['code']

            address = ''
            if 'address' in request.GET and request.GET['address'] != '':
                address = request.GET['address']

            if project_id:
                works = works.filter(project_id=project_id)

            if property_id:
                works = works.filter(property_id=property_id)

            if jobtype_id:
                works = works.filter(workstypes__isnull=False, workstypes__type__id=jobtype_id).distinct()

            if team_id:
                works = works.filter(Q(leader__id=team_id) |
                                     Q(support1__id=team_id) |
                                     Q(support2__id=team_id) |
                                     Q(support3__id=team_id) |
                                     Q(support4__id=team_id) |
                                     Q(support5__id=team_id)).distinct()

            if status_id:
                if status_id == 1:
                    works = works.filter(is_completed=True)
                else:
                    works = works.filter(is_completed=False)

            if creator_id:
                works = works.filter(created_by__id=creator_id)

            if initial_date and end_date:
                works = works.filter(date__range=(initial_date, end_date))

            if initial_date and not end_date:
                works = works.filter(date__gte=initial_date)

            if not initial_date and end_date:
                works = works.filter(date__lte=end_date)

            if code:
                works = works.filter(id__icontains=code)

            if address:
                works = works.filter(address__icontains=address)

            paging = MiPaginator(works, 17)

            p = 1
            if 'page' in request.GET:
                p = int(request.GET['page'])
            page = paging.page(p)

            data['paging'] = paging
            data['ranges_paging'] = paging.pages_range(p)
            data['page'] = page
            data['works'] = page.object_list

            data['projects'] = Projects.objects.all().order_by('name') if not data['is_hotwire'] else Projects.objects.filter(works__customer__id=CUSTOMER_HOTWIRE_ID).distinct().order_by('name')
            data['properties'] = Properties.objects.all().order_by('name') if not data['is_hotwire'] else Properties.objects.filter(works__customer__id=CUSTOMER_HOTWIRE_ID).distinct().order_by('name')
            data['jobtypes'] = JobTypes.objects.all().order_by('name')
            data['teams'] = Users.objects.filter(group=USER_GROUP_TECHNICIAN_ID)
            creators = Users.objects.exclude(id__in=USER_ADMIN_DEVELOPERS_IDS).order_by('user__username')
            data['creators'] = creators if not data['is_hotwire'] else creators.filter(group=USER_GROUP_HOTWIRE_ID)

            data['projectid'] = project_id if project_id else 0
            data['propertyid'] = property_id if property_id else 0
            data['jobtypeid'] = jobtype_id if jobtype_id else 0
            data['teamid'] = team_id if team_id else 0
            data['creatorid'] = creator_id if creator_id else 0
            data['statusid'] = str(status_id) if status_id else 0
            data['code'] = code if code else ''
            data['address'] = address if address else ''
            data['initial_date'] = initial_date.strftime('%m-%d-%Y') if initial_date else ''
            data['end_date'] = end_date.strftime('%m-%d-%Y') if end_date else ''

            if project_id or property_id or jobtype_id or team_id or creator_id or status_id or code or address or initial_date or end_date:
                data['is_search'] = True
                data['count_of_works'] = works.count()

            return render(request, 'works/view.html', data)
