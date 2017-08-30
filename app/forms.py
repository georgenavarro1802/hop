import os
from django import forms
from django.contrib.auth.models import Group

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


class JobTypesForm(forms.Form):
    name = forms.CharField(max_length=200, required=True, label='Name')


class CustomersForm(forms.Form):
    name = forms.CharField(max_length=300, required=True, label='Name')
    phone = forms.CharField(max_length=100, required=False, label='Phone')
    email = forms.CharField(max_length=300, required=False, label='Email')


class UsersForm(forms.Form):
    group = forms.ModelChoiceField(Group.objects.all(), label='Group', required=True,
                                   widget=forms.Select(attrs={'class': 'imp-50'}))
    username = forms.CharField(max_length=100, required=True, label='Username',
                               widget=forms.TextInput(attrs={'class': 'imp-50'}))
    first_name = forms.CharField(max_length=300, required=True, label='FirstName')
    last_name = forms.CharField(max_length=300, required=True, label='LastName')
    email = forms.CharField(max_length=300, required=False, label='Email')
    phone = forms.CharField(max_length=100, required=False, label='Phone',
                            widget=forms.TextInput(attrs={'class': 'imp-50'}))
    avatar = ExtFileField(label='Avatar', help_text='Max size allowed 5Mb in jpeg, jpg, gif, png format',
                          required=False, ext_whitelist=(".jpeg", ".jpg", ".gif", ".png"), max_upload_size=5242880)


class WorksForm(forms.Form):
    project = forms.ModelChoiceField(Projects.objects.all().order_by('name'), label='Project',
                                     required=True, widget=forms.Select(attrs={'class': 'imp-50'}))
    customer = forms.ModelChoiceField(Customers.objects.order_by('name'), label='Customer',
                                      required=True, widget=forms.Select(attrs={'class': 'imp-50'}))
    address = forms.CharField(required=True, label='Address')
    date = forms.CharField(required=False, label='Date', widget=forms.TextInput(attrs={'class': 'imp-20',
                                                                                       'placeholder': 'mm-dd-yyyy'}))
    initial_time = forms.CharField(label='Start Time', widget=forms.TextInput(attrs={'class': 'imp-20',
                                                                                     'placeholder': 'hh:mm'}))
    notes = forms.CharField(required=True, label='Notes')
    # Asign Lead and Support Team
    leader = forms.ModelChoiceField(Users.objects.exclude(user__id=1).order_by('user__username'), label='Leader',
                                    required=True, widget=forms.Select(attrs={'class': 'imp-50',
                                                                              'separator': 'Team Support'}))
    support1 = forms.ModelChoiceField(Users.objects.exclude(user__id=1).order_by('user__username'), label='Support 1',
                                      required=False, widget=forms.Select(attrs={'class': 'imp-50'}))
    support2 = forms.ModelChoiceField(Users.objects.exclude(user__id=1).order_by('user__username'), label='Support 2',
                                      required=False, widget=forms.Select(attrs={'class': 'imp-50'}))
    support3 = forms.ModelChoiceField(Users.objects.exclude(user__id=1).order_by('user__username'), label='Support 3',
                                      required=False, widget=forms.Select(attrs={'class': 'imp-50'}))
    support4 = forms.ModelChoiceField(Users.objects.exclude(user__id=1).order_by('user__username'), label='Support 4',
                                      required=False, widget=forms.Select(attrs={'class': 'imp-50'}))
    support5 = forms.ModelChoiceField(Users.objects.exclude(user__id=1).order_by('user__username'), label='Support 5',
                                      required=False, widget=forms.Select(attrs={'class': 'imp-50'}))
