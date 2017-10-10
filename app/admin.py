from django.contrib import admin

from app.models import Projects, JobTypes, Customers, Works, Users, WorksTypes, JobRequestsTypes, JobRequests


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )

admin.site.register(Projects, ProjectsAdmin)


class JobTypesAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )

admin.site.register(JobTypes, JobTypesAdmin)


class CustomersAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    search_fields = ('name', 'phone', 'email')

admin.site.register(Customers, CustomersAdmin)


class WorksAdmin(admin.ModelAdmin):
    list_display = ('project', 'address', 'date', 'initial_time', 'end_time', 'is_completed', 'customer', 'evaluation')
    search_fields = ('project__name', 'address', 'customer__name')
    list_filter = ('is_completed', 'evaluation')

admin.site.register(Works, WorksAdmin)


class UsersAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'color_hoe_header', 'color_hoe_right_header', 'color_hoeapp_container', 'avatar')
    search_fields = ('user__username', 'user__first_name', 'phone')

admin.site.register(Users, UsersAdmin)


class WorksTypesAdmin(admin.ModelAdmin):
    list_display = ('work', 'type')
    search_fields = ('work', 'type')
    list_filter = ('type', )

admin.site.register(WorksTypes, WorksTypesAdmin)


class JobRequestsAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'notes')
    search_fields = ('email', 'phone')

admin.site.register(JobRequests, JobRequestsAdmin)


class JobRequestsTypesAdmin(admin.ModelAdmin):
    list_display = ('job_request', 'type')
    search_fields = ('job_request', 'type')
    list_filter = ('type', )

admin.site.register(JobRequestsTypes, JobRequestsTypesAdmin)
