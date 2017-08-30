from rest_framework import routers, serializers, viewsets
from rest_framework import filters
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response

from app.models import *
from rest.serializers import *

# ViewSets define the view behavior.
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


class WorksTypesViewSet(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = WorksTypes.objects.all()
    serializer_class = WorksTypesSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
