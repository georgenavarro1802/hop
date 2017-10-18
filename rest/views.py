from datetime import datetime

from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from hop.settings import EMAIL_ACTIVE, CONTACT_EMAILS
from rest.functions import send_html_mail
from rest.serializers import *
from app.models import JobRequests, JobTypes


class ProjectsViewSet(mixins.ListModelMixin, generics.GenericAPIView):

    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializers

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class JobTypesViewSet(mixins.ListModelMixin, generics.GenericAPIView):

    queryset = JobTypes.objects.all().order_by('name')
    serializer_class = JobTypesSerializer
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CustomersViewSet(mixins.ListModelMixin, generics.GenericAPIView):

    queryset = Customers.objects.all()
    serializer_class = CustomersSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UsersViewSet(mixins.ListModelMixin, generics.GenericAPIView):

    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class WorksViewSet(mixins.ListModelMixin, generics.GenericAPIView):

    queryset = Works.objects.all()
    serializer_class = WorksSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class WorksViewDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                      generics.GenericAPIView):

    queryset = Works.objects.all()
    serializer_class = WorksSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():

                work = self.get_object()

                if 'latitude' in request.data and request.data['latitude']:
                    latitude = request.data['latitude']
                    work.latitude_register = float(latitude)

                if 'longitude' in request.data and request.data['longitude']:
                    longitude = request.data['longitude']
                    work.longitude_register = float(longitude)

                if 'register_time' in request.data and request.data['register_time']:
                    register_time = request.data['register_time']
                    work.register_time = "{}".format(register_time)

                if 'report' in request.data and request.data['report']:
                    report = request.data['report']
                    work.report = report

                if 'job_types' in request.data and request.data['job_types']:
                    job_types = request.data['job_types'].split(',')
                    for job_type_id in job_types:
                        if job_type_id and JobTypes.objects.filter(id=job_type_id).exists():
                            job_type = JobTypes.objects.filter(id=job_type_id)[0]
                            works_types = WorksTypes(work=work, type=job_type)
                            works_types.save()

                if 'photo1' in request.data:
                    uploaded_file = request.data['photo1']
                    imgdata = uploaded_file.file
                    if imgdata:
                        print("name {}".format(uploaded_file._name))
                        new_file_name = "{}_photo1.{}".format(work.address, uploaded_file.name)
                        data = ContentFile(imgdata.read(), name=new_file_name)
                        work.photo1 = data

                if 'photo2' in request.data:
                    uploaded_file = request.data['photo2']
                    imgdata = uploaded_file.file
                    if imgdata:
                        new_file_name = "{}_photo2.{}".format(work.address, uploaded_file.name)
                        data = ContentFile(imgdata.read(), name=new_file_name)
                        work.photo2 = data

                if 'photo3' in request.data:
                    uploaded_file = request.data['photo3']
                    imgdata = uploaded_file.file
                    if imgdata:
                        new_file_name = "{}_photo3.{}".format(work.address, uploaded_file.name)
                        data = ContentFile(imgdata.read(), name=new_file_name)
                        work.photo3 = data

                if 'photo4' in request.data:
                    uploaded_file = request.data['photo4']
                    imgdata = uploaded_file.file
                    if imgdata:
                        new_file_name = "{}_photo4.{}".format(work.address, uploaded_file.name)
                        data = ContentFile(imgdata.read(), name=new_file_name)
                        work.photo4 = data

                if 'sign' in request.data:
                    uploaded_file = request.data['sign']
                    imgdata = uploaded_file.file
                    if imgdata:
                        new_file_name = "{}_sign.{}".format(work.address, uploaded_file.name)
                        data = ContentFile(imgdata.read(), name=new_file_name)
                        work.sign = data
                        work.is_completed = True

                if 'evaluation' in request.data and request.data['evaluation']:
                    evaluation = int(request.data['evaluation'])
                    work.evaluation = evaluation

                if 'end_time' in request.data and request.data['end_time']:
                    end_time = request.data['end_time']
                    work.end_time = end_time

                work.save()

                if EMAIL_ACTIVE and work.end_time:
                    send_html_mail("HOP App - Complete Works",
                                   "emails/work_complete.html",
                                   {'work': work},
                                   CONTACT_EMAILS)

                return Response({"Message": "Success"})

        except Exception as ex:
            print("ex {}".format(ex))
            return Response({"Message": "Error"})


class CompleteWorksView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                        generics.GenericAPIView):

    queryset = Works.objects.all()
    serializer_class = WorksSerializer

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():

                work = self.get_object()
                work.is_completed = True

                if 'end_time' in request.data and request.data['end_time']:
                    work.end_time = request.data['end_time']

                work.save()
                return Response({"message": "Success"})

        except Exception as ex:
            print("ex {}".format(ex))
            return Response({"Message": "Error"})


class JobRequestsDetail(generics.GenericAPIView):
    queryset = JobRequests.objects.all()
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):

        try:
            with transaction.atomic():

                email = ''
                phone = ''
                notes = ''

                if 'email' in request.data and request.data['email']:
                    email = request.data['email']

                if 'phone' in request.data and request.data['phone']:
                    phone = request.data['phone']

                if 'notes' in request.data and request.data['notes']:
                    notes = request.data['notes']

                if email and phone and notes:
                    job_request = JobRequests(email=email, phone=phone, notes=notes)
                    job_request.save()

                    if 'types' in request.data and request.data['types']:
                        for type in request.data['types'].split(','):
                            if type and JobTypes.objects.filter(id=type).exists():
                                job_type = JobTypes.objects.filter(id=type).first()
                                job_request_types = JobRequestsTypes(job_request=job_request, type=job_type)
                                job_request_types.save()
                        job_request.save()

                        if EMAIL_ACTIVE and job_request:
                            send_html_mail("HOP App - Job Requests",
                                           "emails/job_request.html",
                                           {'job_request': job_request},
                                           CONTACT_EMAILS)

                        return Response({"message": "Success"})

            return Response({"message": "failure", "error": "missing required fields"})

        except Exception as ex:
            print(ex)


class UserWorksView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                    generics.GenericAPIView):

    queryset = Works.objects.all()
    serializer_class = WorksSerializer

    def order_by_time_str(self, works_array):
        sorted([tuple(map(int, d.initial_time.split(":"))) for d in works_array])
        return works_array

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = Users.objects.get(user=self.request.user)
        works_array = [x for x in Works.objects.filter(leader=user, is_completed=False, date=datetime.now().date())]
        works = [x.id for x in self.order_by_time_str(works_array)]
        return reversed(Works.objects.filter(id__in=works))

    def get(self, request, *args, **kwargs):
        return Response([WorksSerializer(x).data for x in self.get_queryset()])


class WorksTypesViewSet(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = WorksTypes.objects.all()
    serializer_class = WorksTypesSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
