from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render

from app.functions import (NOMBRE_INSTITUCION, bad_json, ok_json, MiPaginator, CUSTOMER_CREATE_NEW_CUSTOMER_ID)
from app.models import Users, Projects, Works, Customers, JobRequests, JobTypes


def adduserdata(request, data):

    data['user'] = user = request.user
    if not Users.objects.filter(user=user).exists():
        myuser = Users(user=user)
        myuser.save()
    else:
        myuser = Users.objects.get(user=user)
    data['myuser'] = myuser

    data['currenttime'] = datetime.now()
    data['nombreinstitucion'] = NOMBRE_INSTITUCION
    data['remoteaddr'] = request.META['REMOTE_ADDR']

    data['is_administrator'] = myuser.is_admin()
    data['is_technician'] = myuser.is_technician()
    data['is_dispatch'] = myuser.is_distpach()
    data['is_hotwire'] = False

    data['customer_create_new_customer_id'] = CUSTOMER_CREATE_NEW_CUSTOMER_ID


@login_required(redirect_field_name='ret', login_url='/login')
def index(request):
    data = {'title': 'Hop Platform'}
    adduserdata(request, data)

    works = Works.objects.order_by('-created_at')
    data['number_projects'] = Projects.objects.count()
    data['number_customers'] = Customers.objects.count()
    data['number_works'] = number_total_works = works.count()

    data['last_five_works'] = works[:5]

    # Top 5 Job Types mos used in projects
    list = []
    for j in JobTypes.objects.filter(workstypes__isnull=False, workstypes__work__is_completed=True).distinct():
        list.append((j.get_number_works_completed(), j.name))

    list_jobtypes_used_projects = sorted(list, reverse=True)[:6]

    data['jobtype_name_1'] = list_jobtypes_used_projects[0][1]
    data['jobtype_name_2'] = list_jobtypes_used_projects[1][1]
    data['jobtype_name_3'] = list_jobtypes_used_projects[2][1]
    data['jobtype_name_4'] = list_jobtypes_used_projects[3][1]
    data['jobtype_name_5'] = list_jobtypes_used_projects[4][1]
    data['jobtype_name_6'] = list_jobtypes_used_projects[5][1]

    data['jobtype_value_1'] = round(list_jobtypes_used_projects[0][0] / number_total_works * 100) if number_total_works else 0
    data['jobtype_value_2'] = round(list_jobtypes_used_projects[1][0] / number_total_works * 100) if number_total_works else 0
    data['jobtype_value_3'] = round(list_jobtypes_used_projects[2][0] / number_total_works * 100) if number_total_works else 0
    data['jobtype_value_4'] = round(list_jobtypes_used_projects[3][0] / number_total_works * 100) if number_total_works else 0
    data['jobtype_value_5'] = round(list_jobtypes_used_projects[4][0] / number_total_works * 100) if number_total_works else 0
    data['jobtype_value_6'] = round(list_jobtypes_used_projects[5][0] / number_total_works * 100) if number_total_works else 0

    if data['is_dispatch']:
        return HttpResponseRedirect('/works')

    return render_to_response("dashboard.html", data)


def login_user(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'].lower(), password=request.POST['password'])
        if user is not None:
            if not user.is_active:
                return HttpResponseRedirect("/login?ret=" + request.POST['ret'] + "&error=3")
            else:
                login(request, user)
                return HttpResponseRedirect(request.POST['ret'])
        else:
            return HttpResponseRedirect("/login?ret=" + request.POST['ret'] + "&error=1")
    else:
        ret = '/'
        if 'ret' in request.GET:
            ret = request.GET['ret']
        return render_to_response("login.html",
                                  {
                                      "title": "Login",
                                      "return_url": ret,
                                      "error": request.GET['error'] if 'error' in request.GET else "",
                                      "request": request,
                                      "currenttime": datetime.now()
                                  })


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


# APIs
def set_color_hoe_header(request):
    myuser = Users.objects.get(user=request.user)
    try:
        with transaction.atomic():
            myuser.color_hoe_header = int(request.POST['obj'].split("logo-bg")[1])
            myuser.save()
            return ok_json()
    except Exception:
        return bad_json(error=1)


def set_color_hoe_right_header(request):
    myuser = Users.objects.get(user=request.user)
    try:
        with transaction.atomic():
            myuser.color_hoe_right_header = int(request.POST['obj'].split("header-bg")[1])
            myuser.save()
            return ok_json()
    except Exception:
        return bad_json(error=1)


def set_color_hoeapp_container(request):
    myuser = Users.objects.get(user=request.user)
    try:
        with transaction.atomic():
            myuser.color_hoeapp_container = int(request.POST['obj'].split("lpanel-bg")[1])
            myuser.save()
            return ok_json()
    except Exception:
        return bad_json(error=1)


def job_requests(request):
    data = {'title': 'Job Requests'}
    adduserdata(request, data)

    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']

            if action == 'delete':
                job_request = JobRequests.objects.get(pk=int(request.POST['id']))
                try:
                    with transaction.atomic():
                        if job_request.jobrequeststypes_set.exists():
                            job_request.jobrequeststypes_set.all().delete()
                        job_request.delete()
                        return ok_json(data={'redirect_url': '/job_requests',
                                             'msg': 'You have successfully deleted the JOB REQUEST.'})
                except Exception:
                    return bad_json(error=3)

        return bad_json(error=0)

    else:

        if 'action' in request.GET:
            if 'action' in request.GET:
                action = request.GET['action']

                if action == 'delete':
                    try:
                        data['title'] = 'Delete Job Request'
                        data['job_request'] = JobRequests.objects.get(pk=request.GET['id'])
                        data['is_delete'] = True
                        return render(request, 'job_requests/delete.html', data)
                    except Exception:
                        pass

    job_request = JobRequests.objects.order_by('-created_at')
    paging = MiPaginator(job_request, 17)

    p = 1
    if 'page' in request.GET:
        p = int(request.GET['page'])
    page = paging.page(p)

    data['paging'] = paging
    data['ranges_paging'] = paging.pages_range(p)
    data['page'] = page
    data['job_requests'] = page.object_list

    return render_to_response('job_requests/view.html', data)
