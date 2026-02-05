from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Session, Attendance, InstructorProfile

@login_required
def instructor_sessions(request):
    profile = InstructorProfile.objects.get(user=request.user)

    sessions = Session.objects.filter(
        group__instructor=profile
    )

    return render(request, 'attendance/sessions.html', {
        'sessions': sessions
    })

@login_required
def mark_attendance(request, session_id):
    session = get_object_or_404(Session, id=session_id)

    students = session.group.students.all()

    if request.method == "POST":
        for student in students:
            present = request.POST.get(f"student_{student.id}") == "on"

            Attendance.objects.update_or_create(
                session=session,
                student=student,
                defaults={'is_present': present}
            )

    attendances = Attendance.objects.filter(session=session)

    return render(request, 'attendance/mark.html', {
        'session': session,
        'students': students,
        'attendances': attendances
    })
