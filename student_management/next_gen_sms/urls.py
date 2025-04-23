from django.urls import path, include
from .views import notifications_view, mark_notification_read
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import (
    custom_logout,
    delete_task,
    events_list,
    add_event,
    edit_event,
    upload_certification,
)
from next_gen_sms.views import (
    marks_update,
    marks_delete,
    marks_list,
    marks_detail,
)
from next_gen_sms.views import ExamManagementView

app_name = "next_gen_sms"

urlpatterns = [
    # 🔐 Authentication (Login, Logout, Password Reset)
    path("accounts/", include("django.contrib.auth.urls")),

    # 🏠 Dashboard & Profile
    path("", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("profile/update/", views.update_profile, name="update_profile"),
    path("profile/update-section/<str:section>/", views.update_profile_section, name="update_profile_section"),

    # 📘 Courses
    path('courses/', views.manage_courses, name='manage_courses'),
    path('courses/list/', views.student_courses, name='student_courses'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('courses/enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),


    # 📋 Tasks
    path("tasks/", views.manage_tasks, name="manage_tasks"),
    path("tasks/toggle/<int:task_id>/", views.toggle_task, name="toggle_task"),
    path("tasks/delete/<int:task_id>/", delete_task, name="delete_task"),

    # 📝 Marks & Attendance
    path("marks/", views.marks_overview, name="marks_overview"),
    path("marks/create/", views.marks_create, name="marks_create"),
    path("marks/<int:pk>/", marks_detail, name="marks_detail"),
    path("marks/<int:marks_id>/update/", marks_update, name="marks_update"),
    path("marks/<int:marks_id>/delete/", marks_delete, name="marks_delete"),
    path("marks/list/", marks_list, name="marks_list"),
    path("attendance/", views.attendance_overview, name="attendance_overview"),
    path("attendance/create/", views.attendance_create, name="attendance_create"),
    path("attendance/<int:pk>/", views.attendance_detail, name="attendance_detail"),
    path("attendance/<int:pk>/edit/", views.attendance_edit, name="attendance_edit"),

    # 🏆 Certifications
    path("certifications/", views.certifications_view, name="certifications"),
    path("upload_certification/", upload_certification, name="upload_certification"),
    path("certifications/delete/<int:cert_id>/", views.delete_certification, name="delete_certification"),

    # 👨‍🏫 Role-Based Dashboards
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("teacher/dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("student/dashboard/api/", views.student_dashboard_api, name="student_dashboard_api"),
    path("admin/dashboard/api/", views.admin_dashboard_api, name="admin_dashboard_api"),

    # 📅 Events
    path("events/", views.events_list, name="events_list"),
    path("events/add/", views.add_event, name="add_event"),
    path("events/edit/<int:event_id>/", views.edit_event, name="edit_event"),
    path("events/delete/<int:event_id>/", views.delete_event, name="delete_event"),

# ⚙️ Settings & Logout
    
    path("edit_user/<int:user_id>/", views.edit_user, name="edit_user"),
    path("manage_users/", views.manage_users, name="manage_users"),
    path("settings/", views.settings_view, name="settings"),
    path("performance/", views.performance_dashboard, name="performance_dashboard"),
    path("delete_account/", views.delete_account, name="delete_account"),
    path("logout/", custom_logout, name="logout"),
 
    
    # 🔔 Notifications
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/<int:notification_id>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/send/', views.send_notification, name='send_notification'),

    # 🏫 Exam Management
    path('exams/', ExamManagementView.as_view(), name='exam_management'),
    path('exams/<int:exam_id>/edit/', ExamManagementView.as_view(), name='exam_edit'),
    path('exams/<int:exam_id>/delete/', ExamManagementView.as_view(), name='exam_delete'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
