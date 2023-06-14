from django.contrib import admin

from Assignment.models import Person, Student, Staff, Course, Assignment, Grading, Submission, \
    RegisteredCourses, RegisteredStudents


class PersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_name', 'first_name', 'email')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('person', 'matric_no')


class StaffAdmin(admin.ModelAdmin):
    list_display = ('person', 'staff_id')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'lecturer')


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'file', 'course', 'lecturer', 'date_given', 'deadline')


class GradingAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'score', 'feedback')


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'grading', 'file', 'date')


class RegisteredCoursesAdmin(admin.ModelAdmin):
    list_display = ('student',)


class RegisteredStudentsAdmin(admin.ModelAdmin):
    list_display = ('course',)


admin.site.register(Person, PersonAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Grading, GradingAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(RegisteredCourses, RegisteredCoursesAdmin)
admin.site.register(RegisteredStudents, RegisteredStudentsAdmin)
