from django import forms
from .models import Course, Review, Category, CourseSection, CourseVideo


class CourseForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)

    class Meta:
        model = Course
        fields = [
            "title",
            "description",
            "category",
            "price",
            "duration_hours",
            "level",
            "start_date",
            "thumbnail",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Course Title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Course Description",
                }
            ),
            "category": forms.Select(attrs={"class": "form-control"}),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "placeholder": "0.00"}
            ),
            "duration_hours": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Hours"}
            ),
            "level": forms.Select(attrs={"class": "form-control"}),
            "start_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "thumbnail": forms.FileInput(attrs={"class": "form-control"}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.RadioSelect(
                choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)]
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Share your thoughts about this course...",
                }
            ),
        }


class CourseSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Search courses by title..."}
        ),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    price_filter = forms.ChoiceField(
        required=False,
        choices=[
            ("", "All Prices"),
            ("free", "Free Courses"),
            ("paid", "Paid Courses"),
        ],
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class CourseSectionForm(forms.ModelForm):
    class Meta:
        model = CourseSection
        fields = ["title", "description", "order"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Section Title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Section Description (optional)",
                }
            ),
            "order": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Order"}),
        }


class CourseVideoForm(forms.ModelForm):
    class Meta:
        model = CourseVideo
        fields = ["title", "description", "video_file", "duration_minutes", "order"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Video Title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Video Description (optional)",
                }
            ),
            "video_file": forms.FileInput(attrs={"class": "form-control", "accept": "video/mp4,.mp4"}),
            "duration_minutes": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Duration (auto-detected if left blank)"}
            ),
            "order": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Order"}),
        }

    def clean_video_file(self):
        video_file = self.cleaned_data["video_file"]
        if video_file:
            # Check file extension
            if not video_file.name.lower().endswith(".mp4"):
                raise forms.ValidationError("Only MP4 video files are allowed.")

            # Check file size
            if video_file.size > 500 * 1024 * 1024:
                raise forms.ValidationError("Video file size must not exceed 500 MB.")

            # Additional validation can be added here
            if video_file.size < 1024:  # Less than 1KB
                raise forms.ValidationError("Video file is too small or corrupted. Please check your file.")

        return video_file

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Auto-detect duration if not provided
        if not instance.duration_minutes and instance.video_file:
            try:
                import subprocess
                import os

                # Get the file path
                file_path = instance.video_file.path

                # Use ffprobe to get duration
                result = subprocess.run(
                    ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                     '-of', 'default=noprint_wrappers=1:nokey=1', file_path],
                    capture_output=True, text=True, timeout=30
                )

                if result.stdout:
                    duration_seconds = float(result.stdout.strip())
                    instance.duration_minutes = int(duration_seconds / 60)
            except Exception as e:
                # If FFmpeg is not available or fails, duration will remain None
                pass

        if commit:
            instance.save()

        return instance
