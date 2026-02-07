from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
import pandas as pd
from django.http import HttpResponse
from .models import InstructorProfile, Group, Student, Session
from .utils import import_students_from_xlsx
from django.contrib import admin

admin.site.site_header = "UPC Attendance System"
admin.site.site_title = "UPC Attendance"
admin.site.index_title = "Management"


@admin.register(InstructorProfile)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    filter_horizontal = ('groups',)

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('group', 'date')

    filter_horizontal = ('absents',)

    # restrict what instructor sees
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(group__instructor__user=request.user)

    # lock fields
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []

        # instructor cannot change these
        return ['group', 'date']

    # block add/delete
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "absents":
            obj_id = request.resolver_match.kwargs.get('object_id')

            if obj_id:
                session = Session.objects.get(id=obj_id)
                kwargs["queryset"] = session.group.students.all()

        return super().formfield_for_manytomany(db_field, request, **kwargs)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'instructor')

    change_form_template = "admin/group_change.html"
    def export_absences(self, request, group_id):
        group = Group.objects.get(id=group_id)

        result = []

        students = group.students.all()
        sessions = Session.objects.filter(group=group)

        for student in students:
            # find sessions where this student is in absents
            absent_sessions = sessions.filter(absents=student)

            dates = [s.date.strftime("%d.%m.%Y") for s in absent_sessions]

            result.append({
                "Student": f"{student.first_name} {student.last_name}",
                "Total absences": len(dates),
                "Dates": ", ".join(dates)
            })

        df = pd.DataFrame(result)

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        response['Content-Disposition'] = f'attachment; filename={group.name}_absence_report.xlsx'

        df.to_excel(response, index=False)

        return response


    def get_urls(self):
        urls = super().get_urls()

        custom = [
    path(
        '<int:group_id>/import/',
        self.admin_site.admin_view(self.import_view),
        name='attendance_group_import',
    ),

    path(
        '<int:group_id>/export/',
        self.admin_site.admin_view(self.export_absences),
        name='attendance_group_export',
    ),
]


        return custom + urls


    def import_view(self, request, group_id):
        if request.method == "POST":
            file = request.FILES['file']
            import_students_from_xlsx(file, group_id)

            self.message_user(request, "Students imported successfully!")

            return redirect(f"/admin/attendance/group/{group_id}/change/")

        return render(request, "admin/import.html")


admin.site.register(Group, GroupAdmin)
