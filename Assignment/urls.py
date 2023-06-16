from django.urls import path

from Assignment import views
from Assignment.views import LoginView, RegisterView, LogoutView, AssignmentView, StudentAssignmentListView, \
    SubmissionView, MarkAssignmentView, SubmitAssignmentView, ProfileView, ForgotPasswordView, ChangePasswordView, \
    AdminView

app_name = 'Assignment'

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("register", RegisterView.as_view(), name="register"),
    path("forgot_password", ForgotPasswordView.as_view(), name="forgot_password"),
    path("forgot_password/<int:id>/change_password", ChangePasswordView.as_view(), name="change_password"),
    path("assignment", AssignmentView.as_view(), name="assignment"),
    path("assignment/<int:ass_id>/students", StudentAssignmentListView.as_view(), name="student_assignment_list"),
    path("assignment/<int:id>/submission", SubmissionView.as_view(), name="submission"),
    path("assignment/<int:sub_id>/submission/mark_assignment", MarkAssignmentView.as_view(), name="mark_assignment"),
    path("assignment/<int:ass_id>/submission/submit_assignment", SubmitAssignmentView.as_view(),
         name="submit_assignment"),
    path("profile", ProfileView.as_view(), name="profile"),
    path("profile/admin", AdminView.as_view(), name="profile_admin"),
    path("profile/admin/add_course", views.add_course, name="add_course"),
]
