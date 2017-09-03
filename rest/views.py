from django.core.files.base import ContentFile

from rest_framework import routers, serializers, viewsets
from rest_framework import filters
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response

from app.models import *
from rest.serializers import *
from rest.functions import *

from datetime import datetime


class ProjectsViewSet(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializers

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class JobTypesViewSet(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = JobTypes.objects.all()
    serializer_class = JobTypesSerializer

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
                    if job_type_id:
                        if JobTypes.objects.filter(id=job_type_id).exists():
                            job_type = JobTypes.objects.filter(id=job_type_id)[0]
                            works_types, created = WorksTypes.objects.get_or_create(work=work, type=job_type)
                            if not created:
                                pass
                            works_types.save()

            imgdata = None
            if 'photo1' in request.data:
                uploaded_file = request.data['photo1']
                imgdata = uploaded_file.file
                if imgdata:
                    print("name {}".format(uploaded_file._name))
                    new_file_name = "{}_photo1.{}".format(work.address, uploaded_file.name)
                    data = ContentFile(imgdata.read(), name=new_file_name)
                    work.photo1 = data
            imgdata = None
            if 'photo2' in request.data:
                uploaded_file = request.data['photo2']
                imgdata = uploaded_file.file
                if imgdata:
                    new_file_name = "{}_photo2.{}".format(work.address, uploaded_file.name)
                    data = ContentFile(imgdata.read(), name=new_file_name)
                    work.photo2 = data
            imgdata = None
            if 'photo3' in request.data:
                uploaded_file = request.data['photo3']
                imgdata = uploaded_file.file
                if imgdata:
                    new_file_name = "{}_photo3.{}".format(work.address, uploaded_file.name)
                    data = ContentFile(imgdata.read(), name=new_file_name)
                    work.photo3 = data
            imgdata = None
            if 'photo4' in request.data:
                uploaded_file = request.data['photo4']
                imgdata = uploaded_file.file
                if imgdata:
                    new_file_name = "{}_photo4.{}".format(work.address, uploaded_file.name)
                    data = ContentFile(imgdata.read(), name=new_file_name)
                    work.photo4 = data
            imgdata = None
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
                print("this is endtime {}".format(end_time))
                work.end_time = end_time
            work.save()
            return Response({"Message": "Success"})
        except Exception as ex:
            print("ex {}".format(ex))
            return Response({"Message":"Error"})


class CompleteWorksView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Works.objects.all()
    serializer_class = WorksSerializer

    def post(self, request, *args, **kwargs):
        work = self.get_object()
        work.is_completed = True
        if 'end_time' in request.data and request.data['end_time']:
            work.end_time = request.data['end_time']
        # Customer rating
        # Customer Signature
        work.save()
        return Response({"message": "Success"})


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
