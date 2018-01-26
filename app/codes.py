from datetime import datetime
from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from easy_pdf.rendering import render_to_pdf_response, fetch_resources

from app.forms import JobTypesForm, InstallationsCodesForm
from app.functions import bad_json, MiPaginator, ok_json
from app.models import JobTypes, InstallationsCodes
from app.views import adduserdata


def views(request):
    data = {'title': 'WORK CODES'}
    adduserdata(request, data)

    if data['is_hotwire'] or data['is_dispatch']:
        return HttpResponseRedirect('/works')

    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']

            if action == 'add':
                f = InstallationsCodesForm(request.POST)
                if f.is_valid():
                    try:
                        with transaction.atomic():

                            if InstallationsCodes.objects.filter(code=f.cleaned_data['code']).exists():
                                return bad_json(message="Work Code already exists with this code. "
                                                        "Please change the code of the Work Code and try again. ")
                            install_code = InstallationsCodes(code=f.cleaned_data['code'],
                                                              description=f.cleaned_data['description'],
                                                              price=f.cleaned_data['price'],
                                                              scope=f.cleaned_data['scope'])
                            install_code.save()
                            return ok_json(data={'redirect_url': '/codes',
                                                 'msg': 'You have successfully created a new Work CODE.'})
                    except Exception:
                        return bad_json(error=1)
                else:
                    return bad_json(message="Form is not valid.")

            if action == 'edit':
                install_code = InstallationsCodes.objects.get(pk=int(request.POST['id']))
                f = InstallationsCodesForm(request.POST)
                if f.is_valid():
                    try:
                        with transaction.atomic():

                            if InstallationsCodes.objects.filter(code=f.cleaned_data['code']).exclude(id=install_code.id).exists():
                                return bad_json(message="Work Code already exists with this code. "
                                                        "Please change the code of the Work Code and try again. ")
                            install_code.code = f.cleaned_data['code']
                            install_code.description = f.cleaned_data['description']
                            install_code.price = f.cleaned_data['price']
                            install_code.scope = f.cleaned_data['scope']
                            install_code.save()
                            return ok_json(data={'redirect_url': '/codes',
                                                 'msg': 'You have successfully edited a new Work CODE.'})
                    except Exception:
                        return bad_json(error=2)
                else:
                    return bad_json(message="Form is not valid.")

            if action == 'delete':
                install_code = InstallationsCodes.objects.get(pk=int(request.POST['id']))
                try:
                    with transaction.atomic():
                        install_code.delete()
                        return ok_json(data={'redirect_url': '/codes',
                                             'msg': 'You have successfully deleted the Work CODE.'})
                except Exception:
                    return bad_json(error=3)

        return bad_json(error=0)

    else:

        if 'action' in request.GET:
            if 'action' in request.GET:
                action = request.GET['action']

                if action == 'add':
                    try:
                        data['title'] = 'New Work Code'
                        data['form'] = InstallationsCodesForm()
                        return render(request, 'codes/add.html', data)
                    except Exception:
                        pass

                if action == 'edit':
                    try:
                        data['title'] = 'Edit Work Code'
                        data['code'] = code = InstallationsCodes.objects.get(pk=request.GET['id'])
                        data['form'] = InstallationsCodesForm(initial={'code': code.code,
                                                              'description': code.description,
                                                              'price': code.price,
                                                              'scope': code.scope})
                        return render(request, 'codes/edit.html', data)
                    except Exception:
                        pass

                if action == 'delete':
                    try:
                        data['title'] = 'Delete Work Code'
                        data['code'] = InstallationsCodes.objects.get(pk=request.GET['id'])
                        data['is_delete'] = True
                        return render(request, 'codes/delete.html', data)
                    except Exception:
                        pass

                if action == 'print':
                    try:
                        data['title'] = 'Print Codes'
                        data['codes'] = InstallationsCodes.objects.order_by('code')
                        data['today'] = datetime.now().date()
                        data['logo_invoice'] = fetch_resources('/static/images/logo_hop_invoice.png', '')
                        return render_to_pdf_response(request, 'codes/print.html', data)

                    except Exception as ex:
                        pass

            return HttpResponseRedirect('/codes')

        else:

            codes = InstallationsCodes.objects.order_by('code')

            search = None
            if 's' in request.GET and request.GET['s'] != '':
                search = request.GET['s']

            if search:
                codes = codes.filter(code__icontains=search).order_by('code')

            paging = MiPaginator(codes, 25)

            p = 1
            if 'page' in request.GET:
                p = int(request.GET['page'])
            page = paging.page(p)

            data['paging'] = paging
            data['ranges_paging'] = paging.pages_range(p)
            data['page'] = page
            data['codes'] = page.object_list
            data['search'] = search if search else ''
            return render(request, 'codes/view.html', data)
