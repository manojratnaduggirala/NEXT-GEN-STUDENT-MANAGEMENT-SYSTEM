from django.test import TestCase
from django.contrib.auth.models import User
from next_gen_sms.models import UserProfile, Course, Attendance, Marks

class UserProfileTest(TestCase):
    def setUp(self):
        """Set up a test user before each test."""
        self.user = User.objects.create_user(username="testuser", password="password123")
    
    def test_user_profile_created(self):
        """Test if a UserProfile is automatically created when a new user is added."""
        profile = UserProfile.objects.get(user=self.user)
        self.assertIsNotNone(profile)

class CourseEnrollmentTest(TestCase):
    def setUp(self):
        """Set up a test user and a course."""
        self.user = User.objects.create_user(username="student1", password="testpass")
        self.course = Course.objects.create(name="Python Programming", description="Learn Python from scratch")

    def test_course_enrollment(self):
        """Test if a user can enroll in a course."""
        self.course.students.add(self.user)
        self.assertIn(self.user, self.course.students.all())

class AttendanceTest(TestCase):
    def setUp(self):
        """Set up a test user."""
        self.user = User.objects.create_user(username="student2", password="testpass")

    def test_attendance_marking(self):
        """Test if attendance is marked correctly."""
        attendance = Attendance.objects.create(student=self.user, status=True)
        self.assertTrue(attendance.status)

class MarksTest(TestCase):
    def setUp(self):
        """Set up a test user."""
        self.user = User.objects.create_user(username="student3", password="testpass")

    def test_marks_entry(self):
        """Test if marks can be added for a student."""
        marks = Marks.objects.create(student=self.user, subject="Math", semester=1, year=1, marks=95)
        self.assertEqual(marks.marks, 95)
