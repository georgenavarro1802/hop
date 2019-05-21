import os
from django import forms

from app.functions import USER_GROUP_TECHNICIAN_ID, USERS_GROUPS, PROJECTS_GROUPS
from app.models import Projects, Customers, Users


class ExtFileField(forms.FileField):
    """
    * max_upload_size - a number indicating the maximum file size allowed for upload.
            500Kb - 524288
            1MB - 1048576
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    t = ExtFileField(ext_whitelist=(".pdf", ".txt"), max_upload_size=)
    """

    def __init__(self, *args, **kwargs):
        ext_whitelist = kwargs.pop("ext_whitelist")
        self.ext_whitelist = [i.lower() for i in ext_whitelist]
        self.max_upload_size = kwargs.pop("max_upload_size")
        super(ExtFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        upload = super(ExtFileField, self).clean(*args, **kwargs)
        if upload:
            size = upload.size
            filename = upload.name
            ext = os.path.splitext(filename)[1]
            ext = ext.lower()

            if size == 0 or ext not in self.ext_whitelist or size > self.max_upload_size:
                raise forms.ValidationError("Tipo de fichero o tamanno no permitido!")


class ProjectsForm(forms.Form):
    name = forms.CharField(max_length=200, required=True, label='Name')
    grupo = forms.ChoiceField(choices=PROJECTS_GROUPS, label='Group', required=True,
                              widget=forms.Select(attrs={'class': 'imp-50'}))


class PropertiesForm(forms.Form):
    project = forms.ModelChoiceField(Projects.objects, label='Project', required=False)
    name = forms.CharField(max_length=300, label='Name')


class JobTypesForm(forms.Form):
    name = forms.CharField(max_length=200, required=True, label='Name')


class InstallationsCodesForm(forms.Form):
    code = forms.CharField(max_length=10, required=True, label='Code', widget=forms.TextInput(attrs={'class': 'imp-30'}))
    description = forms.CharField(max_length=200, required=False, label='Description')
    price = forms.FloatField(initial='0.00', required=False, label='Price', widget=forms.TextInput(attrs={'class': 'imp-30'}))
    scope = forms.CharField(required=False, label='Scopes (separated by commas)', widget=forms.Textarea(attrs={'cols': '2', 'rows': '5'}))


class CustomersForm(forms.Form):
    is_company = forms.BooleanField(required=False, initial=True,
                                    label='Is Company? (checked = Company. no checked = Customer)',
                                    widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    name = forms.CharField(max_length=300, required=True, label='Name')
    phone = forms.CharField(max_length=100, required=False, label='Phone')
    email = forms.CharField(max_length=300, required=False, label='Email')


class UsersForm(forms.Form):
    group = forms.ChoiceField(choices=USERS_GROUPS, label='Group', required=True, widget=forms.Select(attrs={'class': 'imp-50'}))
    username = forms.CharField(max_length=100, required=True, label='Username', widget=forms.TextInput(attrs={'class': 'imp-50'}))
    first_name = forms.CharField(max_length=300, required=True, label='FirstName')
    last_name = forms.CharField(max_length=300, required=True, label='LastName')
    email = forms.CharField(max_length=300, required=False, label='Email')
    phone = forms.CharField(max_length=100, required=False, label='Phone',
                            widget=forms.TextInput(attrs={'class': 'imp-50'}))
    avatar = ExtFileField(label='Avatar', help_text='Max size allowed 5Mb in jpeg, jpg, gif, png format',
                          required=False, ext_whitelist=(".jpeg", ".jpg", ".gif", ".png"), max_upload_size=5242880)
    password = forms.CharField(max_length=300, required=False, label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'imp-100'}))


class WorksForm(forms.Form):
    # Customer Data
    customer = forms.ModelChoiceField(Customers.objects.order_by('name'), label='Customer',
                                      required=False, widget=forms.Select(attrs={'class': 'imp-75 myselect2',
                                                                                 'separator': 'Select Customer or Create New Customer'}))
    customer_name = forms.CharField(max_length=300, required=False, label='Customer Name',
                                    widget=forms.TextInput(attrs={'class': 'form-control imp-75'}))
    customer_email = forms.CharField(max_length=300, required=False, label='Customer Email',
                                     widget=forms.TextInput(attrs={'class': 'form-control imp-75'}))
    customer_phone = forms.CharField(max_length=100, required=False, label='Customer Phone',
                                     widget=forms.TextInput(attrs={'class': 'form-control imp-30'}))

    # Works Details
    # project = forms.ModelChoiceField(Projects.objects.order_by('name'), label='Project',
    #                                  required=True, widget=forms.Select(attrs={'class': 'imp-75 myselect2',
    #                                                                            'separator': 'Work Details'}))
    # property = forms.ModelChoiceField(Properties.objects.order_by('name'), label='Property',
    #                                   required=False, widget=forms.Select(attrs={'class': 'imp-75 myselect2'}))
    address = forms.CharField(required=False, label='Address', widget=forms.Textarea(attrs={'rows': '2', 'cols': '2',
                                                                                            'class': 'form-control'}))
    date = forms.CharField(required=False, label='Date', widget=forms.TextInput(attrs={'class': 'imp-20',
                                                                                       'placeholder': 'mm-dd-yyyy'}))
    initial_time = forms.CharField(required=False, label='Start Time', widget=forms.TextInput(attrs={'class': 'imp-20',
                                                                                                     'placeholder': 'hh:mm'}))
    feedback_email = forms.CharField(required=False, label='Feedback Email', widget=forms.TextInput(attrs={'class': 'imp-100'}))
    notes = forms.CharField(required=False, label='Notes', widget=forms.Textarea(attrs={'rows': '3', 'cols': '2',
                                                                                        'class': 'form-control'}))
    # Wor Team
    leader = forms.ModelChoiceField(Users.objects.filter(group=USER_GROUP_TECHNICIAN_ID), required=False,
                                    widget=forms.Select(attrs={'class': 'imp-50 myselect2',
                                                               'separator': 'Work Team'}), label='Leader')
    support1 = forms.ModelChoiceField(Users.objects.filter(group=USER_GROUP_TECHNICIAN_ID), required=False,
                                      widget=forms.Select(attrs={'class': 'imp-50 myselect2'}), label='Support 1')
    support2 = forms.ModelChoiceField(Users.objects.filter(group=USER_GROUP_TECHNICIAN_ID), required=False,
                                      widget=forms.Select(attrs={'class': 'imp-50 myselect2'}), label='Support 2')
    support3 = forms.ModelChoiceField(Users.objects.filter(group=USER_GROUP_TECHNICIAN_ID), required=False,
                                      widget=forms.Select(attrs={'class': 'imp-50 myselect2'}), label='Support 3')
    # support4 = forms.ModelChoiceField(Users.objects.filter(group=USER_GROUP_TECHNICIAN_ID), required=False,
    #                                   widget=forms.Select(attrs={'class': 'imp-50 myselect2'}), label='Support 4')
    # support5 = forms.ModelChoiceField(Users.objects.filter(group=USER_GROUP_TECHNICIAN_ID), required=False,
    #                                   widget=forms.Select(attrs={'class': 'imp-50 myselect2'}), label='Support 5')


class ChangeAddressForm(forms.Form):
    address = forms.CharField(required=False, label='Address',
                              widget=forms.Textarea(attrs={'rows': '2', 'cols': '2', 'class': 'form-control'}))


class NewLeaderForm(forms.Form):
    leader = forms.ModelChoiceField(Users.objects.filter(group=USER_GROUP_TECHNICIAN_ID), required=False,
                                    widget=forms.Select(attrs={'class': 'imp-50'}), label='Leader')
    support1 = forms.ModelChoiceField(Users.objects.filter(group=USER_GROUP_TECHNICIAN_ID), required=False,
                                      widget=forms.Select(attrs={'class': 'imp-50'}), label='Support 1')
    support2 = forms.ModelChoiceField(Users.objects.filter(group=USER_GROUP_TECHNICIAN_ID), required=False,
                                      widget=forms.Select(attrs={'class': 'imp-50'}), label='Support 2')
    support3 = forms.ModelChoiceField(Users.objects.filter(group=USER_GROUP_TECHNICIAN_ID), required=False,
                                      widget=forms.Select(attrs={'class': 'imp-50'}), label='Support 3')
    # support4 = forms.ModelChoiceField(Users.objects.filter(group=USER_GROUP_TECHNICIAN_ID), required=False,
    #                                 widget=forms.Select(attrs={'class': 'imp-50'}), label='Support 4')
    # support5 = forms.ModelChoiceField(Users.objects.filter(group=USER_GROUP_TECHNICIAN_ID), required=False,
    #                                 widget=forms.Select(attrs={'class': 'imp-50'}), label='Support 5')


class ImportXLSForm(forms.Form):
    file = ExtFileField(label='Select Excel File', help_text='Max size allowed 4Mb (extensions: xls, xlsx)',
                        ext_whitelist=(".xls", ".xlsx"), max_upload_size=4194304, required=False)
