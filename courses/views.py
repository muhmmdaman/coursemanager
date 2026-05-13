from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.utils import timezone
import subprocess
import os
from .models import Course, Enrollment, Review, Category, CourseSection, CourseVideo, VideoProgress, CourseProgress
from .forms import (
    CourseForm,
    ReviewForm,
    CourseSearchForm,
    CourseSectionForm,
    CourseVideoForm,
)


def get_video_duration(video_file_path):
    """Extract video duration in seconds using ffprobe"""
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1:noesc=1',
            video_file_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and result.stdout.strip():
            duration_seconds = float(result.stdout.strip())
            duration_minutes = int(round(duration_seconds / 60))
            return max(1, duration_minutes)  # Minimum 1 minute
    except Exception as e:
        print(f"Error extracting video duration: {e}")

    return None


def home(request):
    featured_courses = Course.objects.all()[:6]
    categories = Category.objects.all()
    context = {
        "featured_courses": featured_courses,
        "categories": categories,
    }
    return render(request, "courses/home.html", context)


def course_list(request):
    courses = Course.objects.select_related("instructor", "category")
    form = CourseSearchForm(request.GET)

    # Search by title
    search_query = request.GET.get("search", "")
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Filter by category
    category_id = request.GET.get("category", "")
    if category_id:
        courses = courses.filter(category_id=category_id)

    # Filter by price
    price_filter = request.GET.get("price_filter", "")
    if price_filter == "free":
        courses = courses.filter(price=0)
    elif price_filter == "paid":
        courses = courses.filter(price__gt=0)

    context = {
        "courses": courses,
        "form": form,
        "search_query": search_query,
    }
    return render(request, "courses/course_list.html", context)


def course_detail(request, pk):
    course = get_object_or_404(
        Course.objects.select_related("instructor", "category"), pk=pk
    )
    reviews = course.reviews.all().select_related("student")
    average_rating = course.get_average_rating()
    review_count = course.get_review_count()

    user_enrolled = False
    user_reviewed = False
    if request.user.is_authenticated:
        user_enrolled = Enrollment.objects.filter(
            student=request.user, course=course
        ).exists()
        user_reviewed = Review.objects.filter(
            student=request.user, course=course
        ).exists()

    context = {
        "course": course,
        "reviews": reviews,
        "average_rating": average_rating,
        "review_count": review_count,
        "user_enrolled": user_enrolled,
        "user_reviewed": user_reviewed,
    }
    return render(request, "courses/course_detail.html", context)


@login_required
def create_course(request):
    if not request.user.is_instructor():
        messages.error(request, "Only instructors can create courses.")
        return redirect("home")

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, "Course created successfully!")
            return redirect("course_detail", pk=course.pk)
    else:
        form = CourseForm()

    return render(request, "courses/create_course.html", {"form": form})


@login_required
def update_course(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if course.instructor != request.user:
        messages.error(request, "You can only edit your own courses.")
        return redirect("course_detail", pk=pk)

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully!")
            return redirect("course_detail", pk=course.pk)
    else:
        form = CourseForm(instance=course)

    return render(
        request, "courses/update_course.html", {"form": form, "course": course}
    )


@login_required
@require_http_methods(["POST"])
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if course.instructor != request.user:
        messages.error(request, "You can only delete your own courses.")
        return redirect("course_detail", pk=pk)

    course_title = course.title
    course.delete()
    messages.success(request, f'Course "{course_title}" has been deleted.')
    return redirect("dashboard")


@login_required
@require_http_methods(["POST"])
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if not request.user.is_student():
        messages.error(request, "Only students can enroll in courses.")
        return redirect("course_detail", pk=pk)

    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user, course=course
    )

    if created:
        course.students_count += 1
        course.save()
        messages.success(
            request, f'You have successfully enrolled in "{course.title}"!'
        )
    else:
        messages.info(request, "You are already enrolled in this course.")

    return redirect("course_detail", pk=pk)


@login_required
@require_http_methods(["POST"])
def unenroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    enrollment = Enrollment.objects.filter(student=request.user, course=course).first()

    if enrollment:
        enrollment.delete()
        course.students_count = max(0, course.students_count - 1)
        course.save()
        messages.success(request, f'You have unenrolled from "{course.title}".')
    else:
        messages.error(request, "You are not enrolled in this course.")

    return redirect("course_detail", pk=pk)


@login_required
def add_review(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if not request.user.is_student():
        messages.error(request, "Only students can review courses.")
        return redirect("course_detail", pk=pk)

    enrollment = Enrollment.objects.filter(student=request.user, course=course).exists()
    if not enrollment:
        messages.error(request, "You must be enrolled in this course to review it.")
        return redirect("course_detail", pk=pk)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.student = request.user
            review.save()
            messages.success(request, "Your review has been posted!")
            return redirect("course_detail", pk=pk)
    else:
        # Check if user already reviewed
        existing_review = Review.objects.filter(
            student=request.user, course=course
        ).first()
        if existing_review:
            form = ReviewForm(instance=existing_review)
        else:
            form = ReviewForm()

    return render(request, "courses/add_review.html", {"form": form, "course": course})


@login_required
def add_section(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if course.instructor != request.user:
        messages.error(request, "You can only add sections to your own courses.")
        return redirect("course_detail", pk=pk)

    if request.method == "POST":
        form = CourseSectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.course = course
            section.save()
            messages.success(request, "Section added successfully!")
            return redirect("course_detail", pk=pk)
    else:
        form = CourseSectionForm()

    return render(request, "courses/add_section.html", {"form": form, "course": course})


@login_required
def edit_section(request, pk):
    section = get_object_or_404(CourseSection, pk=pk)
    course = section.course

    if course.instructor != request.user:
        messages.error(request, "You can only edit sections of your own courses.")
        return redirect("course_detail", pk=course.pk)

    if request.method == "POST":
        form = CourseSectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            messages.success(request, "Section updated successfully!")
            return redirect("course_detail", pk=course.pk)
    else:
        form = CourseSectionForm(instance=section)

    return render(
        request,
        "courses/edit_section.html",
        {"form": form, "section": section, "course": course},
    )


@login_required
@require_http_methods(["POST"])
def delete_section(request, pk):
    section = get_object_or_404(CourseSection, pk=pk)
    course = section.course

    if course.instructor != request.user:
        messages.error(request, "You can only delete sections from your own courses.")
        return redirect("course_detail", pk=course.pk)

    section_title = section.title
    section.delete()
    messages.success(request, f'Section "{section_title}" has been deleted.')
    return redirect("course_detail", pk=course.pk)


@login_required
def upload_video(request, section_id):
    section = get_object_or_404(CourseSection, pk=section_id)
    course = section.course

    if course.instructor != request.user:
        messages.error(
            request, "You can only upload videos to your own course sections."
        )
        return redirect("course_detail", pk=course.pk)

    if request.method == "POST":
        form = CourseVideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.section = section

            # Auto-detect duration if not provided
            if not video.duration_minutes:
                try:
                    video_path = video.video_file.path
                    duration = get_video_duration(video_path)
                    if duration:
                        video.duration_minutes = duration
                        messages.info(request, f"Duration auto-detected: {duration} minutes")
                    else:
                        messages.warning(request, "Could not auto-detect duration. Please enter manually.")
                except Exception as e:
                    messages.warning(request, f"Duration auto-detection failed: {str(e)}")

            video.save()
            messages.success(request, "Video uploaded successfully!")
            return redirect("course_detail", pk=course.pk)
    else:
        form = CourseVideoForm()

    return render(
        request,
        "courses/upload_video.html",
        {"form": form, "section": section, "course": course},
    )


@login_required
@require_http_methods(["POST"])
def delete_video(request, pk):
    video = get_object_or_404(CourseVideo, pk=pk)
    section = video.section
    course = section.course

    if course.instructor != request.user:
        messages.error(request, "You can only delete videos from your own courses.")
        return redirect("course_detail", pk=course.pk)

    video_title = video.title
    video.delete()
    messages.success(request, f'Video "{video_title}" has been deleted.')
    return redirect("course_detail", pk=course.pk)


@login_required
def watch_video(request, pk):
    video = get_object_or_404(CourseVideo, pk=pk)
    course = video.section.course

    enrollment = Enrollment.objects.filter(student=request.user, course=course).exists()
    is_instructor = course.instructor == request.user

    if not enrollment and not is_instructor:
        messages.error(request, "You must be enrolled in this course to watch videos.")
        return redirect("course_detail", pk=course.pk)

    # Create or get progress records for students
    video_progress = None
    course_progress = None
    overall_progress = 0

    if enrollment:  # Only for enrolled students, not instructors
        # Get or create enrollment record
        enrollment_obj = Enrollment.objects.get(student=request.user, course=course)

        # Create or get course progress
        course_progress, _ = CourseProgress.objects.get_or_create(
            student=request.user,
            course=course,
            enrollment=enrollment_obj,
        )

        # Create or get video progress
        video_progress, _ = VideoProgress.objects.get_or_create(
            student=request.user,
            video=video,
        )

        # Calculate overall progress
        overall_progress = course_progress.get_overall_progress_percentage()

    context = {
        "video": video,
        "course": course,
        "section": video.section,
        "video_progress": video_progress,
        "course_progress": course_progress,
        "overall_progress": overall_progress,
        "is_student": enrollment,
        "is_instructor": is_instructor,
    }
    return render(request, "courses/watch_video.html", context)


def serve_video(request, file_path):
    """Serve video files with proper headers"""
    from django.http import FileResponse
    from django.core.exceptions import PermissionDenied
    import os

    video = get_object_or_404(CourseVideo, video_file=file_path)
    course = video.section.course

    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(student=request.user, course=course).exists()
        is_instructor = course.instructor == request.user

        if not enrollment and not is_instructor:
            raise PermissionDenied
    else:
        raise PermissionDenied

    file_path_full = video.video_file.path
    if os.path.exists(file_path_full):
        response = FileResponse(open(file_path_full, 'rb'), content_type='video/mp4')
        response['Content-Disposition'] = f'inline; filename="{video.title}.mp4"'
        return response
    else:
        raise FileNotFoundError


@login_required
@require_http_methods(["POST"])
def update_video_progress(request):
    """API endpoint to update video watch progress"""
    try:
        import json
        data = json.loads(request.body)
        video_id = data.get('video_id')
        watch_time = data.get('watch_time', 0)
        is_completed = data.get('is_completed', False)

        video = get_object_or_404(CourseVideo, pk=video_id)
        course = video.section.course

        # Verify enrollment
        enrollment = Enrollment.objects.filter(student=request.user, course=course).exists()
        if not enrollment:
            return JsonResponse({'success': False, 'message': 'Not enrolled'}, status=403)

        # Update video progress
        video_progress, _ = VideoProgress.objects.get_or_create(
            student=request.user,
            video=video
        )

        # Only increase watch time, don't decrease
        video_progress.watch_time_seconds = max(video_progress.watch_time_seconds, int(watch_time))

        if is_completed:
            video_progress.is_completed = True
            video_progress.completed_at = timezone.now()

        video_progress.save()

        # Update course progress
        enrollment_obj = Enrollment.objects.get(student=request.user, course=course)
        course_progress, _ = CourseProgress.objects.get_or_create(
            student=request.user,
            course=course,
            enrollment=enrollment_obj
        )

        overall_progress = course_progress.get_overall_progress_percentage()

        return JsonResponse({
            'success': True,
            'video_progress': video_progress.get_progress_percentage(),
            'course_progress': overall_progress,
            'message': 'Progress updated'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)
