import pandas as pd
from .models import Student, Group

def import_students_from_xlsx(file, group_id):
    df = pd.read_excel(file)

    group = Group.objects.get(id=group_id)

    for _, row in df.iterrows():
        student, created = Student.objects.get_or_create(
            first_name=row['name'],
            last_name=row['surname']
        )

        student.groups.add(group)
