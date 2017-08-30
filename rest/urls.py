from django.conf.urls import url
from rest_framework import routers
from django.conf.urls import url, include


from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


from rest.views import *

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # Projects
    url(r'^projects/', ProjectsViewSet.as_view(), name='api_projects'),
    # Work Types
    url(r'^job_types/', JobTypesViewSet.as_view(), name='api_job_types'),
    # Customers
    url(r'^customers/', CustomersViewSet.as_view(), name='api_customers'),
    # Users
    url(r'^users/', UsersViewSet.as_view(), name='api_users'),
    # Works
    url(r'^user_works/', UserWorksView.as_view(), name='user_works_api_detail'),
    url(r'^complete_works/(?P<pk>[0-9]+)/$', CompleteWorksView.as_view(), name='complete_works_api_detail'),
    url(r'^works/(?P<pk>[0-9]+)/$', WorksViewDetail.as_view(), name='works_api_detail'),
    url(r'^works/', WorksViewSet.as_view(), name='works_api'),
    # WorksTypes
    url(r'^works_types/', WorksTypesViewSet.as_view(), name='api_works'),
    # Tokens
    url(r'^token/', obtain_jwt_token),
    url(r'^refresh/', refresh_jwt_token),


]
