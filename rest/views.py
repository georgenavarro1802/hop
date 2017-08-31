from rest_framework import routers, serializers, viewsets
from rest_framework import filters
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response

from app.models import *
from rest.serializers import *

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
            if 'longitude' in request.data and request.data['longitude']:
                longitude = request.data['longitude']
            if 'time' in request.data and request.data['time']:
                time = request.data['time']
            print("{}:{}".format(float(latitude), float(longitude)))
            work.latitude_register = float(latitude)
            work.longitude_register = float(longitude)
            work.register_time = "{}".format(time)
            work.save()
            return Response({"Message": "Success"})
        except Exception as ex:
            print("ex {}".format(ex))
            return Response({"Message":"Error"})


class CompleteWorksView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Works.objects.all()
    serializer_class = WorksSerializer

    def get(self, request, *args, **kwargs):
        work = self.get_object()
        work.is_completed = True
        work.save()
        return Response({"message": "Success"})


class UserWorksView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Works.objects.all()
    serializer_class = WorksSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = Users.objects.get(user=self.request.user)
        return Works.objects.filter(leader=user, is_completed=False)

    def get(self, request, *args, **kwargs):
        return Response([WorksSerializer(x).data for x in self.get_queryset()])


class WorksTypesViewSet(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = WorksTypes.objects.all()
    serializer_class = WorksTypesSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
