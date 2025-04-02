from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from next_gen_sms.models import CustomUser, UserProfile, Attendance, Marks, Course, DailyTask, Event, Certification

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Roles & Permissions', {'fields': ('role', 'is_staff', 'is_active', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

# User Profile Admin
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'department')
    search_fields = ('user__username', 'phone_number')

# Attendance Admin
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('student__username',)

# Marks Admin
class MarksAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'semester', 'year', 'marks')
    list_filter = ('semester', 'year')
    search_fields = ('student__username', 'subject')

# Course Admin
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# Daily Task Admin
class DailyTaskAdmin(admin.ModelAdmin):
    list_display = ('student', 'task_description', 'completed', 'created_at')
    list_filter = ('completed', 'created_at')
    search_fields = ('student__username', 'task_description')

# Event Admin
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location', 'organizer')
    search_fields = ('title', 'organizer__username')
    list_filter = ('date', 'time')

# Certification Admin
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('student', 'title', 'issued_date')
    search_fields = ('student__username', 'title')
    list_filter = ('issued_date',)

# Register models in Django Admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Marks, MarksAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(DailyTask, DailyTaskAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Certification, CertificationAdmin)