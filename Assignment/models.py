from django.contrib.auth.models import User
from django.db import models


class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Student(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    matric_no = models.CharField(max_length=20)

    def __str__(self):
        return self.matric_no


class Staff(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.person}"


class Course(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    lecturer = models.ForeignKey(Staff, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code}"


class Assignment(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='Assignment/files')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date_given = models.DateTimeField()
    deadline = models.DateTimeField()

    def __str__(self):
        return f"{self.title}"


class Grading(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    feedback = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.score}"


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grading = models.ForeignKey(Grading, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    file = models.FileField(upload_to='Assignment/submission')
    date = models.DateField()

    def __str__(self):
        return f"{self.student}"


class RegisteredCourses(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return f"{self.student}"


class RegisteredStudents(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return f"{self.course}"