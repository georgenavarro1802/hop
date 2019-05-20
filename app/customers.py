from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from app.forms import CustomersForm
from app.functions import bad_json, MiPaginator, ok_json
from app.models import Customers
from app.views import adduserdata


def views(request):
    data = {'title': 'CUSTOMERS'}
    adduserdata(request, data)

    if data['is_dispatch']:
        return HttpResponseRedirect('/works')

    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']

            if action == 'add':
                f = CustomersForm(request.POST)
                if f.is_valid():
                    try:
                        with transaction.atomic():

                            email = f.cleaned_data['email']
                            if email and Customers.objects.filter(email=email).exists():
                                return bad_json(message="Email already exists in other Customer. "
                                                        "Please change the email of the customer and try again.")
                            customer = Customers(name=f.cleaned_data['name'],
                                                 phone=f.cleaned_data['phone'],
                                                 email=email,
                                                 is_company=f.cleaned_data['is_company'])
                            customer.save()
                            return ok_json(data={'redirect_url': '/customers',
                                                 'msg': 'You have successfully created a new CUSTOMER.'})
                    except Exception:
                        return bad_json(error=1)
                else:
                    return bad_json(message="Form is not valid.")

            if action == 'edit':
                customer = Customers.objects.get(pk=int(request.POST['id']))
                f = CustomersForm(request.POST)
                if f.is_valid():
                    try:
                        with transaction.atomic():

                            email = f.cleaned_data['email']
                            if email and Customers.objects.filter(email=email).exclude(id=customer.id).exists():
                                return bad_json(message="Email already exists in other Customer. "
                                                        "Please change the email of the customer and try again.")
                            customer.name = f.cleaned_data['name']
                            customer.phone = f.cleaned_data['phone']
                            customer.email = email
                            customer.is_company = f.cleaned_data['is_company']
                            customer.save()
                            return ok_json(data={'redirect_url': '/customers',
                                                 'msg': 'You have successfully edited the CUSTOMER.'})
                    except Exception:
                        return bad_json(error=2)
                else:
                    return bad_json(message="Form is not valid.")

            if action == 'delete':
                customer = Customers.objects.get(pk=int(request.POST['id']))
                try:
                    with transaction.atomic():
                        customer.works_set.all().delete()
                        customer.delete()
                        return ok_json(data={'redirect_url': '/customers',
                                             'msg': 'You have successfully deleted the CUSTOMER.'})
                except Exception:
                    return bad_json(error=3)

        return bad_json(error=0)

    else:

        if 'action' in request.GET:
            if 'action' in request.GET:
                action = request.GET['action']

                if action == 'add':
                    try:
                        data['title'] = 'New Customer'
                        data['form'] = CustomersForm()
                        return render(request, 'customers/add.html', data)
                    except Exception:
                        pass

                if action == 'edit':
                    try:
                        data['title'] = 'Edit Customer'
                        data['customer'] = customer = Customers.objects.get(pk=request.GET['id'])
                        data['form'] = CustomersForm(initial={'name': customer.name,
                                                              'phone': customer.phone,
                                                              'email': customer.email,
                                                              'is_company': True if customer.is_company else False})
                        return render(request, 'customers/edit.html', data)
                    except Exception:
                        pass

                if action == 'delete':
                    try:
                        data['title'] = 'Delete Customer'
                        data['customer'] = Customers.objects.get(pk=request.GET['id'])
                        data['is_delete'] = True
                        return render(request, 'customers/delete.html', data)
                    except Exception:
                        pass

            return HttpResponseRedirect('/customers')

        else:

            customers = Customers.objects.order_by('name')

            search = None
            if 's' in request.GET and request.GET['s'] != '':
                search = request.GET['s']

            if search:
                customers = customers.filter(name__icontains=search)

            paging = MiPaginator(customers, 25)

            p = 1
            if 'page' in request.GET:
                p = int(request.GET['page'])
            page = paging.page(p)

            data['paging'] = paging
            data['ranges_paging'] = paging.pages_range(p)
            data['page'] = page
            data['customers'] = page.object_list

            return render(request, 'customers/view.html', data)
