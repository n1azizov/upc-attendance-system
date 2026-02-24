from django.db import models
from django.contrib.auth.models import User

class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Group(models.Model):
    name = models.CharField(max_length=100)
    instructor = models.ForeignKey(
        InstructorProfile,
        on_delete=models.CASCADE,
        related_name='groups'
    )

    def __str__(self):
        return f"{self.name} - {self.instructor}"


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name='students')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Session(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date = models.DateField()

    absents = models.ManyToManyField(
        Student,
        blank=True,
        related_name='absent_sessions'
    )

    class Meta:
        unique_together = ('group', 'date')

    def __str__(self):
        return f"{self.group} - {self.date}"

