from django.conf.urls import url
from rest_framework import routers
from django.conf.urls import url, include


from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


from rest.views import *

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # Projects
    url(r'^projects/', ProjectsViewSet.as_view(), name='projects'),
    # Work Types
    url(r'^job_types/', JobTypesViewSet.as_view(), name='job_types'),
    # Customers
    url(r'^customers/', CustomersViewSet.as_view(), name='customers'),
    # Users
    url(r'^users/', UsersViewSet.as_view(), name='users'),
    # Works
    url(r'^works/', WorksViewSet.as_view(), name='works'),
    # WorksTypes
    url(r'^works_types/', WorksTypesViewSet.as_view(), name='works'),


    url(r'^token/', obtain_jwt_token),
    url(r'^refresh/', refresh_jwt_token),


]
