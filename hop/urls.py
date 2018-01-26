"""activos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include


from app import views, projects, jobtypes, customers, users, reports, works, properties, codes

urlpatterns = [

    # ADMIN
    url(r'^admin/', admin.site.urls),

    # INDEX (Dashboard)
    url(r'^$', views.index, name='dashboard'),

    # LOGIN
    url(r'^login$', views.login_user, name='login'),

    # LOGOUT
    url(r'^logout$', views.logout_user, name='logout'),

    # PROJECTS
    url(r'^projects$', projects.views, name='projects'),

    # PROPERTIES
    url(r'^properties$', properties.views, name='properties'),

    # JOB TYPES
    url(r'^jobtypes$', jobtypes.views, name='jobtypes'),

    # JOB REQUESTS
    url(r'^job_requests$', views.job_requests, name='job_requests'),

    # CUSTOMERS
    url(r'^customers$', customers.views, name='customers'),

    # USERS
    url(r'^users$', users.views, name='users'),

    # STATS
    url(r'^reports$', reports.views, name='reports'),

    # WORKS
    url(r'^works$', works.views, name='works'),

    # WORK CODES
    url(r'^codes$', codes.views, name='codes'),

    # APIs Colors
    url(r'^set_color_hoe_header$', views.set_color_hoe_header, name='set_color_hoe_header'),
    url(r'^set_color_hoe_right_header$', views.set_color_hoe_right_header, name='set_color_hoe_right_header'),
    url(r'^set_color_hoeapp_container$', views.set_color_hoeapp_container, name='set_color_hoeapp_container'),

    # APIs
    url(r'^api/', include('rest.urls'), name='apis'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
