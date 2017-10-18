from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models, router
from django.db.models import Q
from django.db.models.deletion import Collector

from app.functions import (USER_GROUP_ADMINISTRATOR_ID, USER_GROUP_TECHNICIAN_ID, USER_GROUP_HOTWIRE_ID,
                           EVALUATION_TYPES, USERS_GROUPS, DEFAULT_DISPATCH_ID, PROJECTS_GROUPS, PROJECT_GROUP_HOP)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        abstract = True

    def can_delete(self):
        """
            Selects which fields of the base model can be deleted
        """
        if self._get_pk_val():
            seen_objs = Collector(router.db_for_write(self.__class__, instance=self))
            seen_objs.collect([self])
            if len(seen_objs.data) > 1:
                raise ValidationError("Sorry, cannot be deleted. {}".format(seen_objs.data))

    def delete(self, **kwargs):
        """
            Deletes fields from base model
        """
        assert self._get_pk_val() is not None, "Object %s cannot be deleted because %s is null." % (
            self._meta.object_name, self._meta.pk.attname)
        seen_objs = Collector(router.db_for_write(self.__class__, instance=self))
        seen_objs.collect([self])
        self.can_delete()
        seen_objs.delete()

    def save(self, **kwargs):
        models.Model.save(self)


class Projects(BaseModel):
    name = models.CharField(max_length=200)
    grupo = models.IntegerField(choices=PROJECTS_GROUPS, default=PROJECT_GROUP_HOP)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        db_table = 'projects'
        unique_together = ('name', )

    def has_relations(self):
        return self.works_set.exists()

    def get_number_works(self):
        if self.has_relations():
            return self.works_set.count()
        return 0

    def get_number_works_completed(self):
        if self.has_relations():
            return self.works_set.filter(is_completed=True).count()
        return 0

    def get_number_works_incompleted(self):
        if self.has_relations():
            return self.works_set.filter(is_completed=False).count()
        return 0


class JobTypes(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Job Type'
        verbose_name_plural = 'Job Types'
        db_table = 'job_types'
        unique_together = ('name', )

    def has_relations(self):
        return self.workstypes_set.exists()

    def get_number_works(self):
        if self.has_relations():
            return self.workstypes_set.count()
        return 0

    def get_number_works_completed(self):
        if self.has_relations():
            return self.workstypes_set.filter(work__is_completed=True).count()
        return 0

    def get_number_works_incompleted(self):
        if self.has_relations():
            return self.workstypes_set.filter(work__is_completed=False).count()
        return 0


class Customers(BaseModel):
    name = models.CharField(max_length=300)
    phone = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.email)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        db_table = 'customers'
        unique_together = ('email', )

    def has_relations(self):
        return self.works_set.exists()

    def get_number_works(self):
        if self.has_relations():
            return self.works_set.count()
        return 0

    def get_number_works_completed(self):
        if self.has_relations():
            return self.works_set.filter(is_completed=True).count()
        return 0

    def get_number_works_incompleted(self):
        if self.has_relations():
            return self.works_set.filter(is_completed=False).count()
        return 0


class Users(BaseModel):
    user = models.ForeignKey(User)
    group = models.IntegerField(choices=USERS_GROUPS, default=USER_GROUP_TECHNICIAN_ID)
    phone = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.FileField(upload_to='avatars/', max_length=100, blank=True, null=True)
    # Interface preferences
    color_hoe_header = models.IntegerField(default=1)
    color_hoe_right_header = models.IntegerField(default=1)
    color_hoeapp_container = models.IntegerField(default=1)

    def __str__(self):
        return "{}".format(self.user)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'Users Profile'
        db_table = 'users_profiles'
        unique_together = ('user', )

    def complete_name(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    def download_avatar(self):
        return self.avatar.url

    def user_group_name(self):
        if self.group == USER_GROUP_ADMINISTRATOR_ID:
            mygroup = "Admin"
        elif self.group == USER_GROUP_TECHNICIAN_ID:
            mygroup = "Technician"
        elif self.group == USER_GROUP_HOTWIRE_ID:
            mygroup = "Hotwire"
        else:
            mygroup = "N/A"
        return mygroup

    def is_admin(self):
        return self.group == USER_GROUP_ADMINISTRATOR_ID

    def is_technician(self):
        return self.group == USER_GROUP_TECHNICIAN_ID

    def is_hotwire(self):
        return self.group == USER_GROUP_HOTWIRE_ID

    def is_distpach(self):
        return self.group == USER_GROUP_TECHNICIAN_ID and self.id == DEFAULT_DISPATCH_ID

    def has_relations(self):
        return self.leader.exists() or \
               self.support1.exists() or \
               self.support2.exists() or \
               self.support3.exists() or \
               self.support4.exists() or \
               self.support5.exists()

    def get_number_works(self):
        if self.has_relations():
            return Works.objects.filter(Q(leader=self) |
                                        Q(support1=self) |
                                        Q(support2=self) |
                                        Q(support3=self) |
                                        Q(support4=self) |
                                        Q(support5=self)).count()
        return 0

    def get_number_works_completed(self):
        if self.has_relations():
            return Works.objects.filter(Q(leader=self) |
                                        Q(support1=self) |
                                        Q(support2=self) |
                                        Q(support3=self) |
                                        Q(support4=self) |
                                        Q(support5=self), is_completed=True).count()
        return 0

    def get_number_works_incompleted(self):
        if self.has_relations():
            return Works.objects.filter(Q(leader=self) |
                                        Q(support1=self) |
                                        Q(support2=self) |
                                        Q(support3=self) |
                                        Q(support4=self) |
                                        Q(support5=self), is_completed=False).count()
        return 0


class Works(BaseModel):
    project = models.ForeignKey(Projects)
    address = models.TextField()
    date = models.DateField(blank=True, null=True)
    initial_time = models.CharField(max_length=10, blank=True, null=True)

    # Users Leader and Support
    leader = models.ForeignKey(Users, related_name='leader', blank=True, null=True)
    support1 = models.ForeignKey(Users, related_name='support1', blank=True, null=True)
    support2 = models.ForeignKey(Users, related_name='support2', blank=True, null=True)
    support3 = models.ForeignKey(Users, related_name='support3', blank=True, null=True)
    support4 = models.ForeignKey(Users, related_name='support4', blank=True, null=True)
    support5 = models.ForeignKey(Users, related_name='support5', blank=True, null=True)

    # Time and Position when technician register his time and complete the job
    register_time = models.CharField(max_length=10, blank=True, null=True)
    latitude_register = models.FloatField(default=0, blank=True, null=True)
    longitude_register = models.FloatField(default=0, blank=True, null=True)
    end_time = models.CharField(max_length=10, blank=True, null=True)

    # Reports
    report = models.TextField(blank=True, null=True)
    photo1 = models.FileField(upload_to='photos/', blank=True, null=True)
    photo2 = models.FileField(upload_to='photos/', blank=True, null=True)
    photo3 = models.FileField(upload_to='photos/', blank=True, null=True)
    photo4 = models.FileField(upload_to='photos/', blank=True, null=True)

    is_completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    # Customer
    customer = models.ForeignKey(Customers, blank=True, null=True)
    evaluation = models.IntegerField(default=0, choices=EVALUATION_TYPES)
    sign = models.FileField(upload_to='signs/', blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.project, self.address)

    class Meta:
        verbose_name = u'Work'
        verbose_name_plural = u'Works'
        db_table = 'works'
        unique_together = ('project', 'address')

    def repr_id(self):
        return str(self.id).zfill(4)

    def download_photo1(self):
        if self.photo1:
            return self.photo1.url
        return ''

    def download_photo2(self):
        if self.photo2:
            return self.photo2.url
        return ''

    def download_photo3(self):
        if self.photo3:
            return self.photo3.url
        return ''

    def download_photo4(self):
        if self.photo4:
            return self.photo4.url
        return ''

    def download_signature(self):
        if self.sign:
            return self.sign.url
        return ''

    def get_my_job_types(self):
        if self.workstypes_set.exists():
            return [x.type for x in self.workstypes_set.all().order_by('type__name')]
        return None


class WorksTypes(BaseModel):
    work = models.ForeignKey(Works)
    type = models.ForeignKey(JobTypes)

    def __str__(self):
        return "{} - {}".format(self.work, self.type)

    class Meta:
        verbose_name = 'Work - Type'
        verbose_name_plural = 'Works - Types '
        db_table = 'works_types'
        unique_together = ('work', 'type')


class JobRequests(BaseModel):
    email = models.CharField(max_length=200, blank=True, null=True, verbose_name='Email')
    phone = models.CharField(max_length=100, blank=True, null=True, verbose_name='Phone')
    notes = models.TextField(blank=True, null=True, verbose_name='Notes')

    def __str__(self):
        return "Job Request: {}".format(self.email)

    class Meta:
        verbose_name = 'Job Request'
        verbose_name_plural = 'Job Requests'
        db_table = 'job_requests'

    def get_my_job_request_types(self):
        return self.jobrequeststypes_set.all()


class JobRequestsTypes(BaseModel):
    job_request = models.ForeignKey(JobRequests)
    type = models.ForeignKey(JobTypes)

    def __str__(self):
        return "{} - {}".format(self.job_request, self.type)

    class Meta:
        verbose_name = 'Job Request - Type'
        verbose_name_plural = 'Job Requests - Types '
        db_table = 'job_requests_types'
        unique_together = ('job_request', 'type')
