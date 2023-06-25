from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from Assignment.functions import upload_student, upload_course, upload_staff
from Assignment.models import Person, Student, Staff, Course, Assignment, Submission, RegisteredCourses, Grading, \
    RegisteredStudents


class LoginView(View):
    template_name = "Assignment/login.html"

    def get(self, request):
        # Go to the register page
        return render(request, self.template_name)

    def post(self, request):
        # Check if form is submitting
        if request.method == "POST":
            # Collect inputs
            username = request.POST.get("username").strip()
            password = request.POST.get("password")

            # Authenticate user
            user = authenticate(username=username, password=password)

            # Check if user exist
            if user is not None:
                # Login user
                login(request, user)
                # Redirect to learning page
                return HttpResponseRedirect(reverse("Assignment:assignment"))
            else:
                # Send error message
                messages.error(request, "Invalid credentials")
                # Redirect to login page
                return HttpResponseRedirect(reverse("Assignment:login"))


class RegisterView(View):
    template_name = "Assignment/register.html"

    def get(self, request):
        # Go to the register page
        return render(request, self.template_name)

    def post(self, request):
        # Check if form is submitting
        if request.method == "POST":
            # Collect inputs
            # Get user input
            file = request.FILES.get('file')
            file_type = request.POST.get('type')

            if file_type == "student":
                try:
                    upload_student(file)
                except Exception:
                    messages.error(request, "Error uploading file")
                    return HttpResponseRedirect(reverse("Attendance:register"))
            elif file_type == "staff":
                try:
                    upload_staff(file)
                except Exception:
                    messages.error(request, "Error uploading file")
                    return HttpResponseRedirect(reverse("Attendance:register"))
            elif file_type == "course":
                try:
                    upload_course(file)
                except Exception:
                    messages.error(request, "Error uploading file")
                    return HttpResponseRedirect(reverse("Attendance:register"))

class ForgotPasswordView(View):
    template_name = "Assignment/forgot_password.html"

    def get(self, request):
        # Go to the register page
        return render(request, self.template_name)

    def post(self, request):
        # Check if form is submitting
        if request.method == "POST":
            # Collect inputs
            username = request.POST.get("username").strip()

            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                person = Person.objects.get(user=user)
                return HttpResponseRedirect(reverse("Assignment:change_password", args=(person.id,)))
            else:
                messages.error(request, "User does not exist")
                return HttpResponseRedirect(reverse("Assignment:forgot_password"))


class ChangePasswordView(View):
    template_name = "Assignment/change_password.html"

    def get(self, request, id):
        # Go to the register page
        return render(request, self.template_name)

    def post(self, request, id):
        person = Person.objects.get(id=id)
        # Check if form is submitting
        if request.method == "POST":
            # Collect inputs
            password = request.POST.get("password").strip()
            confirm_password = request.POST.get("confirm_password").strip()

            if password == confirm_password:
                person.user.set_password(password)
                person.user.save()
                messages.success(request, "Password update successful")
                return HttpResponseRedirect(reverse("Assignment:login"))
            else:
                messages.error(request, "Password does not match")
                return HttpResponseRedirect(reverse("Assignment:change_password", args=(person.id,)))


class AssignmentView(View):
    template_name = "Assignment/assignment.html"

    @method_decorator(login_required)
    def get(self, request):
        person = Person.objects.get(user=request.user)

        if Staff.objects.filter(person=person).exists():
            lecturer = Staff.objects.get(person=person)
            all_assignments = Assignment.objects.filter(lecturer=lecturer)
            courses = Course.objects.filter(lecturer=lecturer)
            current_user = "staff"
            return render(request, self.template_name,
                          {'assignments': all_assignments, "user": current_user, "person": person, "courses": courses})

        else:
            student = Student.objects.get(person=person)
            reg_courses = RegisteredCourses.objects.get(student=student)
            all_assignments = [
                Assignment.objects.filter(course=course).values() for course in reg_courses.courses.all()
            ]
            all_assignments = [
                {"id": ass[0]["id"], "title": ass[0]["title"], "course": Course.objects.get(id=ass[0]["course_id"]).code, "date_given": ass[0]["date_given"], "deadline": ass[0]["deadline"]} for ass in all_assignments
            ]
            current_user = "student"

            return render(request, self.template_name, {'assignments': all_assignments, "user": current_user, "person": person})

    @method_decorator(login_required)
    def post(self, request):
        person = Person.objects.get(user=request.user)
        lecturer = Staff.objects.get(person=person)
        # Check if form is submitting
        if request.method == "POST":
            # Collect inputs
            course_code = request.POST.get("course_code").strip().upper()
            pdf_title = request.POST.get("pdf_title").strip().upper()
            deadline = request.POST.get("deadline")
            file = request.FILES.get("file")
            print(file)

            course = Course.objects.get(code=course_code)
            Assignment.objects.create(title=pdf_title, file=file, course=course, lecturer=lecturer,
                                      date_given=datetime.now().today(), deadline=deadline)

            # Redirect back to register page
            return HttpResponseRedirect(reverse("Assignment:assignment"))


class StudentAssignmentListView(View):
    template_name = "Assignment/student_assignment_list.html"

    @method_decorator(login_required)
    def get(self, request, ass_id):
        person = Person.objects.get(user=request.user)
        assignment = Assignment.objects.get(id=ass_id)
        all_submission = Submission.objects.filter(assignment=assignment)
        return render(request, self.template_name, {"all_submission": all_submission, "person": person})


class SubmissionView(View):
    template_name = "Assignment/submission.html"

    @method_decorator(login_required)
    def get(self, request, id):
        person = Person.objects.get(user=request.user)

        if Staff.objects.filter(person=person).exists():
            lecturer = Staff.objects.get(person=person)
            current_user = "staff"
            submission = Submission.objects.get(id=id)
            return render(request, self.template_name, {"submission": submission, "user": current_user, "person": person})

        else:
            student = Student.objects.get(person=person)
            current_user = "student"
            assignment = Assignment.objects.get(id=id)
            if Submission.objects.filter(**{"assignment":assignment, "student":student}).exists():
                submission = Submission.objects.get(assignment=assignment, student=student)
                return render(request, self.template_name, {"submission": submission, "user": current_user, "person": person})
            else:
                return render(request, self.template_name, {"assignment": assignment, "user": current_user, "person": person})


class MarkAssignmentView(View):
    template_name = "Assignment/mark_assignment.html"

    @method_decorator(login_required)
    def get(self, request, sub_id):
        person = Person.objects.get(user=request.user)
        submission = Submission.objects.get(id=sub_id)
        return render(request, self.template_name, {"submission": submission, "person": person})

    @method_decorator(login_required)
    def post(self, request, sub_id):
        submission = Submission.objects.get(id=sub_id)

        # Check if form is submitting
        if request.method == "POST":
            # Collect inputs
            score = request.POST.get("score").strip()
            feedback = request.POST.get("feedback").strip()

            submission.grading.score = score
            submission.grading.feedback = feedback
            submission.grading.save()

            return HttpResponseRedirect(reverse("Assignment:submission", args=(submission.id,)))


class SubmitAssignmentView(View):
    template_name = "Assignment/submit_assignment.html"

    @method_decorator(login_required)
    def get(self, request, ass_id):
        person = Person.objects.get(user=request.user)
        student = Student.objects.get(person=person)
        assignment = Assignment.objects.get(id=ass_id)
        if not Submission.objects.filter(**{"assignment":assignment, "student":student}).exists():
            grading = Grading.objects.create(assignment=assignment, student=student)
            submission = Submission.objects.create(assignment=assignment, student=student, grading=grading, date=datetime.now().date())
        else:
            submission = Submission.objects.get(assignment=assignment, student=student)
        return render(request, self.template_name, {"submission": submission, "person": person})

    @method_decorator(login_required)
    def post(self, request, ass_id):
        person = Person.objects.get(user=request.user)
        student = Student.objects.get(person=person)
        assignment = Assignment.objects.get(id=ass_id)
        submission = Submission.objects.get(assignment=assignment, student=student)

        # Check if form is submitting
        if request.method == "POST":
            # Collect inputs
            answer = request.POST.get("answer").strip()
            file = request.FILES.get("file")

            submission.text = answer
            submission.file = file
            submission.save()

            return HttpResponseRedirect(reverse("Assignment:submission", args=(assignment.id,)))


class ProfileView(View):
    template_name = "Assignment/profile.html"

    @method_decorator(login_required)
    def get(self, request):
        person = Person.objects.get(user=request.user)
        if Staff.objects.filter(person=person).exists():
            user = Staff.objects.get(person=person)
            current_user = "staff"
        else:
            user = Student.objects.get(person=person)
            current_user = "student"
        return render(request, self.template_name, {"user": user, "current_user": current_user, "person": person})

    @method_decorator(login_required)
    def post(self, request):
        person = Person.objects.get(user=request.user)
        # Check if form is submitting
        if request.method == "POST":
            # Collect inputs
            email = request.POST.get("email").strip()
            password = request.POST.get("password").strip()
            confirm_password = request.POST.get("confirm_password").strip()

            if email != "":
                person.email = email
                person.save()
                messages.success("Email successfully updated")

            if password == confirm_password:
                request.user.set_password(password)
                request.user.save()
                messages.success(request, "Password update successful")
            else:
                messages.error(request, "Password does not match")

            return HttpResponseRedirect(reverse("Assignment:profile"))


class AdminView(View):
    template_name = "Assignment/profile_admin.html"

    @method_decorator(login_required)
    def get(self, request):
        person = Person.objects.get(user=request.user)

        if Staff.objects.filter(person=person).exists():
            lecturer = Staff.objects.get(person=person)
            all_courses = Course.objects.filter(lecturer=lecturer)
            current_user = "staff"
        else:
            student = Student.objects.get(person=person)
            reg_courses = RegisteredCourses.objects.get(student=student)
            all_courses = reg_courses.courses.all()
            current_user = "student"

        return render(request, self.template_name,
                      {'all_courses': all_courses, "user": current_user, "person": person})

    @method_decorator(login_required)
    def post(self, request):
        person = Person.objects.get(user=request.user)
        lecturer = Staff.objects.get(person=person)
        # Check if form is submitting
        if request.method == "POST":
            # Collect inputs
            course_title = request.POST.get("course_title").strip().upper()
            course_code = request.POST.get("course_code").strip().upper()

            if Course.objects.filter(**{"title": course_title, "code": course_code}).exists():
                messages.error(request, "Course already exists")

            else:
                course = Course.objects.create(title=course_title, code=course_code, lecturer=lecturer)
                RegisteredStudents.objects.create(course=course)
                messages.success(request, "Course successfully registered")

            # Redirect back to register page
            return HttpResponseRedirect(reverse("Assignment:profile_admin"))


def add_course(request):
    person = Person.objects.get(user=request.user)
    student = Student.objects.get(person=person)
    # Check if form is submitting
    if request.method == "POST":
        # Collect inputs
        course_code = request.POST.get("course_code").strip().upper()

        if Course.objects.filter(code=course_code).exists():
            course = Course.objects.get(code=course_code)
            reg_std = RegisteredStudents.objects.get(course=course)
            reg_std.students.add(student)
            reg_course = RegisteredCourses.objects.get(student=student)
            reg_course.courses.add(course)
            messages.error(request, "Course successfully added")

        else:
            messages.error(request, "Course does not exist")

        # Redirect back to register page
        return HttpResponseRedirect(reverse("Assignment:profile_admin"))


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse("Assignment:login"))