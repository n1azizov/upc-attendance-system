from django.db import migrations

def create_instructors_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    group, created = Group.objects.get_or_create(name='Instructors')

    permissions = Permission.objects.filter(
        content_type__app_label='attendance',
        codename__in=[
            'view_session',
            'change_session',
        ]
    )

    group.permissions.set(permissions)
    group.save()

class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_session_absents_delete_attendance'),
    ]

    operations = [
        migrations.RunPython(create_instructors_group),
    ]
