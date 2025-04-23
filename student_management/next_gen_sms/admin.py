from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, 
    UserProfile,
    Attendance,
    Marks,
    Course,
    CourseStudent,
    DailyTask,
    Event,
    Certification,
    CoursePlaylist,
    Notification,
    Exam,
    ExamResult
)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'custom_id', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'custom_id']
    ordering = ['username']

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'profile_image', 'custom_id')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'profile_image', 'custom_id')}),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'phone_number']
    search_fields = ['user__username', 'department']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'timestamp', 'created_by')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('user__username', 'message', 'created_by__username')
    readonly_fields = ('timestamp',)

# Register remaining models with basic admin interface
admin.site.register(Attendance)
admin.site.register(Marks)
admin.site.register(Course)
admin.site.register(CourseStudent)
admin.site.register(DailyTask)
admin.site.register(Event)
admin.site.register(Certification)
admin.site.register(CoursePlaylist)
