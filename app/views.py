from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from app.functions import (NOMBRE_INSTITUCION, bad_json, ok_json)
from app.models import Users, Projects, Works, Customers, WorksTypes


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


@login_required(redirect_field_name='ret', login_url='/login')
def index(request):
    data = {'title': 'Hop Platform'}
    adduserdata(request, data)
    works = Works.objects.all().order_by('-created_at')
    data['number_projects'] = Projects.objects.count()
    data['number_customers'] = Customers.objects.count()
    data['number_works'] = works.count()
    data['last_five_works'] = works[:5]
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
