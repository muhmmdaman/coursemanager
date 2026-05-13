from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Course(models.Model):
    LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="courses",
        limit_choices_to={"role": "instructor"},
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="courses"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    duration_hours = models.IntegerField(help_text="Duration in hours")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="beginner")
    start_date = models.DateTimeField()
    thumbnail = models.ImageField(upload_to="course_thumbnails/", blank=True, null=True)
    students_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["category", "-created_at"]),
            models.Index(fields=["instructor"]),
        ]

    def __str__(self):
        return f"{self.title} by {self.instructor.username}"

    def is_free(self):
        return self.price == 0

    def get_average_rating(self):
        """Calculate average rating from reviews"""
        reviews = self.reviews.all()
        if not reviews.exists():
            return 0
        total_rating = sum(review.rating for review in reviews)
        return round(total_rating / reviews.count(), 2)

    def get_review_count(self):
        return self.reviews.count()


class Enrollment(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="enrollments",
        limit_choices_to={"role": "student"},
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ["student", "course"]
        ordering = ["-enrolled_at"]
        indexes = [
            models.Index(fields=["student", "course"]),
        ]

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        limit_choices_to={"role": "student"},
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["course", "student"]
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["course", "student"]),
        ]

    def __str__(self):
        return f"Review by {self.student.username} for {self.course.title}"


class CourseSection(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="sections"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]
        indexes = [
            models.Index(fields=["course", "order"]),
        ]

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class CourseVideo(models.Model):
    section = models.ForeignKey(
        CourseSection, on_delete=models.CASCADE, related_name="videos"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    video_file = models.FileField(upload_to="course_videos/")
    duration_minutes = models.IntegerField(blank=True, null=True)
    order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]
        indexes = [
            models.Index(fields=["section", "order"]),
        ]

    def __str__(self):
        return f"{self.section.course.title} - {self.section.title} - {self.title}"


class VideoProgress(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="video_progress",
        limit_choices_to={"role": "student"},
    )
    video = models.ForeignKey(
        CourseVideo, on_delete=models.CASCADE, related_name="progress"
    )
    watch_time_seconds = models.IntegerField(default=0)
    last_watched_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ["student", "video"]
        indexes = [
            models.Index(fields=["student", "video"]),
        ]

    def __str__(self):
        return f"{self.student.username} - {self.video.title}"

    def get_progress_percentage(self):
        if not self.video.duration_minutes or self.video.duration_minutes == 0:
            return 0
        total_seconds = self.video.duration_minutes * 60
        return min(100, int((self.watch_time_seconds / total_seconds) * 100))


class CourseProgress(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="course_progress",
        limit_choices_to={"role": "student"},
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="student_progress"
    )
    enrollment = models.OneToOneField(
        Enrollment, on_delete=models.CASCADE, related_name="progress"
    )
    last_watched_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["student", "course"]
        indexes = [
            models.Index(fields=["student", "course"]),
        ]

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

    def get_overall_progress_percentage(self):
        """Calculate course progress from all videos"""
        videos = CourseVideo.objects.filter(section__course=self.course)
        if not videos.exists():
            return 0

        total_progress = 0
        for video in videos:
            try:
                progress = VideoProgress.objects.get(student=self.student, video=video)
                total_progress += progress.get_progress_percentage()
            except VideoProgress.DoesNotExist:
                pass

        return int(total_progress / videos.count())

    def get_completed_videos_count(self):
        return VideoProgress.objects.filter(
            student=self.student,
            video__section__course=self.course,
            is_completed=True
        ).count()

    def get_total_videos_count(self):
        return CourseVideo.objects.filter(section__course=self.course).count()
