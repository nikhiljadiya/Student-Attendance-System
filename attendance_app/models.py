from django.db import models
from datetime import datetime

class Stream(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return str(self.id) + ' - ' + self.name

class Semester(models.Model):
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)

    def __str__(self):
        return str(self.id) + ' - ' + str(self.stream.name) + ' ' + self.name

class Subject(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)

    def __str__(self):
        return str(self.id) + ' - ' + str(self.semester.stream.name) + ' - ' + str(self.semester.name) + ' ' + self.name

class Student(models.Model):
    firstname = models.CharField(max_length=250)
    middlename = models.CharField(max_length=250)
    lastname = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    mobile = models.CharField(max_length=250)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    enrollment_no = models.CharField(max_length=250)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id) + ' - ' + str(self.firstname) + ' ' + str(self.middlename) + ' ' + str(self.lastname) + ' ' + str(self.status)

class Attendance(models.Model):
    date = models.DateField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + str(datetime.strftime(self.date, '%d/%m/%Y')) + ' - ' + str(self.subject.semester.stream.name) + ' - ' + str(self.subject.semester.name) + ' - ' + str(self.subject.name)

class StudentAttendance(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + ' - ' + str(self.student.firstname) + ' ' + str(self.student.middlename) + ' ' + str(self.student.lastname) + ' - ' + str(self.status)
