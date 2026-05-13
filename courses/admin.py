from django.contrib import admin
from .models import Course, Category, Enrollment, Review, CourseSection, CourseVideo, VideoProgress, CourseProgress


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)


class CourseVideoInline(admin.TabularInline):
    model = CourseVideo
    fields = ("title", "order", "duration_minutes", "video_file")
    extra = 1


class CourseSectionInline(admin.TabularInline):
    model = CourseSection
    fields = ("title", "order", "description")
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "instructor",
        "category",
        "price",
        "students_count",
        "level",
        "created_at",
    )
    list_filter = ("category", "level", "price", "created_at")
    search_fields = ("title", "description", "instructor__username")
    readonly_fields = ("students_count", "created_at", "updated_at")
    inlines = [CourseSectionInline]
    fieldsets = (
        ("Course Info", {"fields": ("title", "description", "instructor", "category")}),
        ("Details", {"fields": ("price", "duration_hours", "level", "start_date")}),
        ("Media", {"fields": ("thumbnail",)}),
        ("Stats", {"fields": ("students_count",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrolled_at", "completed")
    list_filter = ("completed", "enrolled_at")
    search_fields = ("student__username", "course__title")
    readonly_fields = ("enrolled_at", "completed_at")
    date_hierarchy = "enrolled_at"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("student__username", "course__title", "comment")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"


@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ("course", "title", "order", "created_at")
    list_filter = ("course", "created_at")
    search_fields = ("course__title", "title")
    readonly_fields = ("created_at", "updated_at")
    inlines = [CourseVideoInline]


@admin.register(CourseVideo)
class CourseVideoAdmin(admin.ModelAdmin):
    list_display = ("section", "title", "order", "duration_minutes", "uploaded_at")
    list_filter = ("section__course", "uploaded_at")
    search_fields = ("section__course__title", "section__title", "title")
    readonly_fields = ("uploaded_at", "updated_at")
    fieldsets = (
        ("Video Info", {"fields": ("section", "title", "description")}),
        ("Media", {"fields": ("video_file", "duration_minutes")}),
        ("Ordering", {"fields": ("order",)}),
        ("Timestamps", {"fields": ("uploaded_at", "updated_at")}),
    )


@admin.register(VideoProgress)
class VideoProgressAdmin(admin.ModelAdmin):
    list_display = ("student", "video", "get_progress", "is_completed", "last_watched_at")
    list_filter = ("is_completed", "last_watched_at")
    search_fields = ("student__username", "video__title")
    readonly_fields = ("last_watched_at",)

    def get_progress(self, obj):
        return f"{obj.get_progress_percentage()}%"
    get_progress.short_description = "Progress"


@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "get_overall_progress", "get_videos_info", "last_watched_at")
    list_filter = ("last_watched_at",)
    search_fields = ("student__username", "course__title")
    readonly_fields = ("last_watched_at",)

    def get_overall_progress(self, obj):
        return f"{obj.get_overall_progress_percentage()}%"
    get_overall_progress.short_description = "Overall Progress"

    def get_videos_info(self, obj):
        completed = obj.get_completed_videos_count()
        total = obj.get_total_videos_count()
        return f"{completed}/{total} videos"
    get_videos_info.short_description = "Videos"
