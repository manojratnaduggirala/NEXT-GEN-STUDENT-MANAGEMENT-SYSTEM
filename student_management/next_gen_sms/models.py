from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.db import models

# Custom User Model
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    profile_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Fix reverse accessor conflicts
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",
        blank=True
    )
    def __str__(self):
        return self.username
# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg', blank=True)
    bio = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

# Attendance Model
class Attendance(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - {self.date} - {'Present' if self.status else 'Absent'}"

# Marks Model
class Marks(models.Model):
    SEMESTER_CHOICES = [
        (1, 'Mid Semester 1'),
        (2, 'Mid Semester 2')
    ]
    YEAR_CHOICES = [
        (1, '1st Year'),
        (2, '2nd Year'),
        (3, '3rd Year'),
        (4, '4th Year')
    ]
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    marks = models.FloatField()
    total_marks = models.FloatField()

    def __str__(self):
        return f"{self.student.username} - {self.subject} - Semester {self.semester} - {self.marks}"

# Courses Model
class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    skills_required = models.TextField()
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='enrolled_courses')

    def __str__(self):
        return self.name
    
class CourseStudent(models.Model):
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_now_add=True)  # Optional: Track enrollment date

    def __str__(self):
        return f"{self.customuser.username} - {self.course.name}"

# Daily Tasks Model
class DailyTask(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task_description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.task_description[:30]}"

# Events Model
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Certifications & Achievements Model
class Certification(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='certifications/')
    issued_date = models.DateField()

    def __str__(self):
        return f"{self.student.username} - {self.title}"
