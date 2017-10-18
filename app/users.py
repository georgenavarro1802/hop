from django.contrib.auth.models import User
from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from app.forms import UsersForm
from app.functions import bad_json, ok_json, DEFAULT_PASSWORD, generate_file_name
from app.models import Users
from app.views import adduserdata


def views(request):
    data = {'title': 'USERS'}
    adduserdata(request, data)

    if data['is_hotwire']:
        return HttpResponseRedirect('/works')

    if request.method == 'POST':

        if 'action' in request.POST:
            action = request.POST['action']

            if action == 'add':
                f = UsersForm(request.POST, request.FILES)
                if f.is_valid():
                    try:
                        with transaction.atomic():

                            if User.objects.filter(username=f.cleaned_data['username']).exists():
                                return bad_json(message="Username already exists in other User. "
                                                        "Please change the username of the user and try again.")

                            if User.objects.filter(email=f.cleaned_data['email']).exists():
                                return bad_json(message="Email already exists in other User. "
                                                        "Please change the email of the user and try again.")

                            django_user = User(username=f.cleaned_data['username'],
                                               first_name=f.cleaned_data['first_name'],
                                               last_name=f.cleaned_data['last_name'],
                                               email=f.cleaned_data['email'])

                            django_user.set_password(DEFAULT_PASSWORD)
                            django_user.save()

                            myuser = Users(user=django_user,
                                           group=f.cleaned_data['group'],
                                           phone=f.cleaned_data['phone'])
                            myuser.save()

                            if 'avatar' in request.FILES:
                                nfile = request.FILES['avatar']
                                nfile._name = generate_file_name("avatar", nfile._name)
                                myuser.avatar = nfile
                                myuser.save()

                            return ok_json(data={'redirect_url': '/users',
                                                 'msg': 'Successfully created a new USER ({})'.format(myuser.user_group_name())})

                    except Exception:
                        return bad_json(error=1)
                else:
                    return bad_json(message="Form is not valid.")

            if action == 'edit':
                myuser = Users.objects.get(pk=int(request.POST['id']))
                django_user = myuser.user
                f = UsersForm(request.POST, request.FILES)
                if f.is_valid():
                    try:
                        with transaction.atomic():

                            if User.objects.filter(username=f.cleaned_data['username']).exclude(id=django_user.id).exists():
                                return bad_json(message="Username already exists in other User. "
                                                        "Please change the username of the user and try again.")

                            if User.objects.filter(email=f.cleaned_data['email']).exclude(id=django_user.id).exists():
                                return bad_json(message="Email already exists in other User. "
                                                        "Please change the email of the user and try again.")

                            django_user.username = f.cleaned_data['username']
                            django_user.first_name = f.cleaned_data['first_name']
                            django_user.last_name = f.cleaned_data['last_name']
                            django_user.email = f.cleaned_data['email']
                            django_user.save()

                            myuser.group = int(f.cleaned_data['group'])
                            myuser.phone = f.cleaned_data['phone']
                            myuser.save()

                            if 'avatar' in request.FILES:
                                nfile = request.FILES['avatar']
                                nfile._name = generate_file_name("avatar", nfile._name)
                                myuser.avatar = nfile
                                myuser.save()

                            return ok_json(data={'redirect_url': '/users',
                                                 'msg': 'Successfully edited the USER ({})'.format(myuser.user_group_name())})
                    except Exception:
                        return bad_json(error=2)
                else:
                    return bad_json(message="Form is not valid.")

            if action == 'delete':
                myuser = Users.objects.get(pk=int(request.POST['id']))
                user = myuser.user
                try:
                    with transaction.atomic():
                        myuser.delete()
                        user.delete()
                        return ok_json(data={'redirect_url': '/users',
                                             'msg': 'You have successfully deleted the USER.'})
                except Exception:
                    return bad_json(error=3)

        return bad_json(error=0)

    else:

        if 'action' in request.GET:
            if 'action' in request.GET:
                action = request.GET['action']

                if action == 'add':
                    try:
                        data['title'] = 'New User'
                        data['form'] = UsersForm()
                        return render(request, 'users/add.html', data)
                    except Exception:
                        pass

                if action == 'edit':
                    try:
                        data['title'] = 'Edit User'
                        data['myuser'] = myuser = Users.objects.get(pk=request.GET['id'])
                        user = myuser.user
                        data['form'] = UsersForm(initial={'username': user.username,
                                                          'first_name': user.first_name,
                                                          'last_name': user.last_name,
                                                          'email': user.email,
                                                          'phone': myuser.phone,
                                                          'group': myuser.group,
                                                          'avatar': myuser.avatar.url if myuser.avatar else ""})
                        return render(request, 'users/edit.html', data)
                    except Exception as ex:
                        pass

                if action == 'delete':
                    try:
                        data['title'] = 'Delete User'
                        data['myuser'] = Users.objects.get(pk=request.GET['id'])
                        data['is_delete'] = True
                        return render(request, 'users/delete.html', data)
                    except Exception as ex:
                        pass

            return HttpResponseRedirect('/users')

        else:

            data['users'] = Users.objects.exclude(user__id=1).order_by('-created_at')
            return render(request, 'users/view.html', data)
