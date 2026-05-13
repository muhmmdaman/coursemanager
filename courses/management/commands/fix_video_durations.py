from django.core.management.base import BaseCommand
from courses.models import CourseVideo
from courses.views import get_video_duration
import os


class Command(BaseCommand):
    help = "Fix video durations by extracting from video files"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force update even if duration already set",
        )

    def handle(self, *args, **options):
        force = options.get("force", False)

        # Get videos to fix
        if force:
            videos = CourseVideo.objects.all()
            self.stdout.write("Force updating ALL videos...")
        else:
            videos = CourseVideo.objects.filter(duration_minutes__isnull=True)
            self.stdout.write("Updating videos with missing duration...")

        fixed_count = 0
        error_count = 0

        for video in videos:
            try:
                video_path = video.video_file.path

                # Check if file exists
                if not os.path.exists(video_path):
                    self.stdout.write(
                        self.style.WARNING(f"File not found: {video.title}")
                    )
                    error_count += 1
                    continue

                # Get duration
                duration = get_video_duration(video_path)

                if duration:
                    old_duration = video.duration_minutes
                    video.duration_minutes = duration
                    video.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"FIXED: {video.title}: {old_duration}min -> {duration}min"
                        )
                    )
                    fixed_count += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f"Could not detect: {video.title}")
                    )
                    error_count += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error processing {video.title}: {str(e)}")
                )
                error_count += 1

        # Summary
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS(f"Fixed: {fixed_count} videos"))
        self.stdout.write(self.style.WARNING(f"Errors: {error_count} videos"))
        self.stdout.write("=" * 50)
