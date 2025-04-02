from django.urls import path, include
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from . import views  # Import all views from views.py
from django.contrib.auth import views as auth_views
from .views import custom_logout

urlpatterns = [
    # Dashboard & Profile
    path("accounts/", include("django.contrib.auth.urls")),
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('admin/', admin.site.urls),

    # Course Enrollment
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('courses/add/', views.add_course, name='add_course'),

    # Tasks
    path('tasks/', views.manage_tasks, name='manage_tasks'),
    path('tasks/toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),

    # Marks & Attendance
    path('marks/', views.marks_overview, name='marks_overview'),
    path('attendance/', views.attendance_overview, name='attendance_overview'),
    path('create/', views.marks_create, name='marks_create'),
    path('update/<int:pk>/', views.marks_update, name='marks_update'),
    path('delete/<int:pk>/', views.marks_delete, name='marks_delete'),
    path('list/', views.marks_list, name='marks_list'),
    path('detail/<int:pk>/', views.marks_detail, name='marks_detail'),

    # Certifications
    path('certifications/', views.upload_certification, name='upload_certification'),
    path('certifications/', views.certifications_view, name='certifications'),
    

    # Dashboards based on roles
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    # Events
    path('events/', views.events_list, name='events_list'),
    path('events/add/', views.add_event, name='add_event'),

    # Settings
    path('settings/', views.user_settings, name='settings'),  # updated to user_settings
    path('delete_account/', views.delete_account, name='delete_account'),
    path('settings/', views.user_settings, name='user_settings'),
    path('logout/', custom_logout, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)