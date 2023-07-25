import pandas as pd
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from Assignment.models import Person, Staff, Student, RegisteredCourses, Course


def upload_staff(file):
    df = pd.read_excel(file)
    data = zip(df.values.tolist())
    for index, i in enumerate(data):
        print(i)
        data2 = []
        for j in i[0]:
            data2.append(j)

        last_name, first_name, email, stf_id = data2

        staff_id = stf_id.strip().upper()
        last_name = last_name.strip().upper()
        first_name = first_name.strip().upper()
        email = email.strip()

        if not User.objects.filter(username=staff_id).exists():
            user = User.objects.create_user(username=staff_id, password="password")

            if str(email) == 'nan':
                person = Person.objects.create(user=user, last_name=last_name, first_name=first_name)
            else:
                person = Person.objects.create(user=user, last_name=last_name, first_name=first_name, email=email)

            staff = Staff.objects.create(person=person, staff_id=staff_id)
            staff.save()


def upload_student(file):
    df = pd.read_excel(file)
    data = zip(df.values.tolist())
    for index, i in enumerate(data):
        data2 = []
        for j in i[0]:
            data2.append(j)

        last_name, first_name, email, matric_no = data2

        matric_no = matric_no.strip().upper()
        last_name = last_name.strip().upper()
        first_name = first_name.strip().upper()
        email = email.strip()

        if not User.objects.filter(username=matric_no).exists():
            user = User.objects.create_user(username=matric_no, password="password")

            if str(email) == 'nan':
                person = Person.objects.create(user=user, last_name=last_name, first_name=first_name)
            else:
                person = Person.objects.create(user=user, last_name=last_name, first_name=first_name, email=email)

            student = Student.objects.create(person=person, matric_no=matric_no)
            student.save()
            RegisteredCourses.objects.create(student=student)


def upload_course(file):
    df = pd.read_excel(file)
    data = zip(df.values.tolist())
    for index, i in enumerate(data):
        data2 = []
        for j in i[0]:
            data2.append(j)

        course_title, course_code, staff_id = data2
        course_title = course_title.strip().upper()
        course_code = course_code.strip().upper()
        staff_id = staff_id.strip().upper()

        if Staff.objects.filter(staff_id=staff_id).exists():
            staff = get_object_or_404(Staff, staff_id=staff_id)

            if not Course.objects.filter(code=course_code).exists():
                course = Course.objects.create(title=course_title, code=course_code, lecturer=staff)
                course.save()

