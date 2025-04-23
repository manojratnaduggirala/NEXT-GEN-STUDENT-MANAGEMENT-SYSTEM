from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from uuid import uuid4
from django.core.validators import MaxValueValidator, MinValueValidator
from next_gen_sms.managers import CustomUserManager

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

# Custom User Model
class CustomUser(AbstractUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )

    custom_id = models.CharField(max_length=15, unique=True, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    profile_image = models.ImageField(upload_to='profile_pics/', default='default.jpg', blank=True, null=True)
    USERNAME_FIELD = 'username'
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.custom_id or self.id})"

    def save(self, *args, **kwargs):
        if not self.custom_id:
            self.custom_id = str(uuid4())[:10]
        super().save(*args, **kwargs)

    def is_student(self):
        return self.role == 'student'

    def is_teacher(self):
        return self.role == 'teacher'

    def is_admin(self):
        return self.role == 'admin'

# User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    achievements = models.TextField(blank=True, null=True, help_text="Enter achievements separated by newlines")
    activities = models.TextField(blank=True, null=True, help_text="Enter recent activities separated by newlines")

    def __str__(self):
        return self.user.username

    @property
    def full_name(self):
        """Returns the user's full name if available, otherwise username"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.user.username

# Attendance
class Attendance(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'}, related_name='attendance_records', null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - {self.date} - {'Present' if self.status else 'Absent'}"
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Attendance Records'

# Marks
class Marks(models.Model):
    SEMESTER_CHOICES = [(1, 'Mid Semester 1'), (2, 'Mid Semester 2')]
    YEAR_CHOICES = [(1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year')]
    marks = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    subject = models.CharField(max_length=100)
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    total_marks = models.FloatField()

    def __str__(self):
        return f"{self.subject} - {self.get_semester_display()} - {self.get_year_display()} - {self.student.username}"

# Courses
class Course(models.Model):
    code = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=200)
    instructor = models.CharField(max_length=100, blank=True, null=True)
    credits = models.IntegerField(blank=True, null=True)
    schedule = models.CharField(max_length=100, blank=True, null=True)
    room = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    youtube_url = models.URLField(max_length=200, blank=True, null=True, verbose_name="YouTube URL")
    skills_required = models.TextField()
    students = models.ManyToManyField(CustomUser, blank=True, related_name='enrolled_courses', limit_choices_to={'role': 'student'})

    def __str__(self):
        return self.name

# Course Enrollments
class CourseStudent(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.name}"

# Daily Tasks
class DailyTask(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    task_description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.task_description[:30]}"

# Events
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Certifications
class Certification(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='certifications/')
    issued_date = models.DateField()

    def __str__(self):
        return f"{self.student.username} - {self.title}"

class CoursePlaylist(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    watched = models.BooleanField(default=False)
    last_watched = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'course')
        verbose_name_plural = 'Course Playlists'

    def __str__(self):
        return f"{self.student.username}'s playlist: {self.course.name}"

class Exam(models.Model):
    EXAM_TYPES = (
        ('midterm', 'Midterm'),
        ('final', 'Final'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
    )
    
    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100)
    max_marks = models.PositiveIntegerField(default=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='created_exams')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date', 'start_time']
        verbose_name_plural = 'Exams'
        
    def __str__(self):
        return f"{self.course.name} - {self.get_exam_type_display()} - {self.date}"

class ExamResult(models.Model):
    GRADE_CHOICES = (
        ('A', 'A (90-100)'),
        ('B', 'B (80-89)'),
        ('C', 'C (70-79)'),
        ('D', 'D (60-69)'),
        ('F', 'F (Below 60)'),
    )
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    marks_obtained = models.FloatField(validators=[MinValueValidator(0)])
    remarks = models.TextField(blank=True)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('exam', 'student')
        ordering = ['-updated_at']

    def save(self, *args, **kwargs):
        # Calculate grade automatically
        percentage = (self.marks_obtained / self.exam.max_marks) * 100
        if percentage >= 90:
            self.grade = 'A'
        elif percentage >= 80:
            self.grade = 'B'
        elif percentage >= 70:
            self.grade = 'C'
        elif percentage >= 60:
            self.grade = 'D'
        else:
            self.grade = 'F'
        super().save(*args, **kwargs)


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    action_url = models.URLField(blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_notifications')

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}"

# Signal handlers for notifications
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=DailyTask)
def notify_task_change(sender, instance, created, **kwargs):
    if created:
        message = f"New task created by {instance.student.username}: {instance.task_description[:50]}"
        url = f"/tasks/manage/"
    else:
        status = "completed" if instance.completed else "marked pending"
        message = f"Task {status} by {instance.student.username}: {instance.task_description[:50]}"
        url = f"/tasks/manage/"

    # Notify all admins
    admins = CustomUser.objects.filter(role='admin')
    for admin in admins:
        Notification.objects.create(
            user=admin,
            message=message,
            action_url=url,
            created_by=instance.student
        )

@receiver(post_save, sender=Attendance)
def notify_attendance_change(sender, instance, created, **kwargs):
    if instance.teacher:  # Only notify if teacher is set
        status = "marked present" if instance.status else "marked absent"
        message = f"Student {instance.student.username} was {status} by {instance.teacher.username}"
        url = f"/attendance/"

        # Notify all admins
        admins = CustomUser.objects.filter(role='admin')
        for admin in admins:
            Notification.objects.create(
                user=admin,
                message=message,
                action_url=url,
                created_by=instance.teacher
            )

@receiver(post_save, sender=UserProfile)
def notify_profile_update(sender, instance, created, **kwargs):
    if not created:  # Only notify on updates
        message = f"Profile updated by {instance.user.username}"
        url = f"/profile/"

        # Notify all admins if student/teacher updated their profile
        if instance.user.is_student() or instance.user.is_teacher():
            admins = CustomUser.objects.filter(role='admin')
            for admin in admins:
                Notification.objects.create(
                    user=admin,
                    message=message,
                    action_url=url,
                    created_by=instance.user
                )
