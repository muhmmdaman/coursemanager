from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("courses/", views.course_list, name="course_list"),
    path("courses/<int:pk>/", views.course_detail, name="course_detail"),
    path("courses/create/", views.create_course, name="create_course"),
    path("courses/<int:pk>/update/", views.update_course, name="update_course"),
    path("courses/<int:pk>/delete/", views.delete_course, name="delete_course"),
    path("courses/<int:pk>/enroll/", views.enroll_course, name="enroll_course"),
    path("courses/<int:pk>/unenroll/", views.unenroll_course, name="unenroll_course"),
    path("courses/<int:pk>/review/", views.add_review, name="add_review"),
    path("courses/<int:pk>/add-section/", views.add_section, name="add_section"),
    path("sections/<int:pk>/edit/", views.edit_section, name="edit_section"),
    path("sections/<int:pk>/delete/", views.delete_section, name="delete_section"),
    path(
        "sections/<int:section_id>/upload-video/",
        views.upload_video,
        name="upload_video",
    ),
    path("videos/<int:pk>/delete/", views.delete_video, name="delete_video"),
    path("videos/<int:pk>/watch/", views.watch_video, name="watch_video"),
    path("api/update-video-progress/", views.update_video_progress, name="update_video_progress"),
]
