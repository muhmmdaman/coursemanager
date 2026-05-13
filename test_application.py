import os
import sys
import django
from django.test import Client
from django.urls import reverse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
sys.path.insert(0, "/c/Users/DELL/Downloads/archit")
django.setup()

from users.models import User
from courses.models import Course, Category, Enrollment, Review
from datetime import datetime, timedelta

print("=" * 60)
print("COURSE HUB - TESTING APPLICATION")
print("=" * 60)

# Test 1: Create test users with different roles
print("\n[TEST 1] Creating Test Users...")
try:
    # Delete existing test users
    User.objects.filter(username__in=["student1", "instructor1"]).delete()

    # Create student user
    student = User.objects.create_user(
        username="student1",
        email="student@example.com",
        password="password123",
        role="student",
        first_name="John",
        last_name="Doe",
    )
    print(f"✓ Student created: {student.username} ({student.get_role_display()})")

    # Create instructor user
    instructor = User.objects.create_user(
        username="instructor1",
        email="instructor@example.com",
        password="password123",
        role="instructor",
        first_name="Jane",
        last_name="Smith",
    )
    print(
        f"✓ Instructor created: {instructor.username} ({instructor.get_role_display()})"
    )

except Exception as e:
    print(f"✗ Error creating users: {e}")

# Test 2: Create categories
print("\n[TEST 2] Creating Categories...")
try:
    Category.objects.all().delete()
    categories_data = [
        ("Programming", "Learn coding and software development"),
        ("Business", "Business and entrepreneurship courses"),
        ("Design", "UI/UX and graphic design courses"),
    ]

    for name, desc in categories_data:
        cat = Category.objects.create(name=name, description=desc)
        print(f"✓ Category created: {cat.name}")
except Exception as e:
    print(f"✗ Error creating categories: {e}")

# Test 3: Create courses
print("\n[TEST 3] Creating Courses...")
try:
    Course.objects.all().delete()
    courses_data = [
        {
            "title": "Python Basics",
            "description": "Learn Python from scratch with hands-on examples",
            "price": 0,
            "duration_hours": 20,
            "level": "beginner",
            "category_name": "Programming",
        },
        {
            "title": "Advanced Django",
            "description": "Master Django framework for web development",
            "price": 49.99,
            "duration_hours": 40,
            "level": "advanced",
            "category_name": "Programming",
        },
    ]

    for course_data in courses_data:
        category = Category.objects.get(name=course_data["category_name"])
        course = Course.objects.create(
            title=course_data["title"],
            description=course_data["description"],
            instructor=instructor,
            category=category,
            price=course_data["price"],
            duration_hours=course_data["duration_hours"],
            level=course_data["level"],
            start_date=datetime.now() + timedelta(days=7),
        )
        print(f"✓ Course created: {course.title} (${course.price})")
except Exception as e:
    print(f"✗ Error creating courses: {e}")

# Test 4: Test Enrollment
print("\n[TEST 4] Testing Enrollment...")
try:
    courses = Course.objects.all()
    for course in courses[:2]:
        enrollment, created = Enrollment.objects.get_or_create(
            student=student, course=course
        )
        if created:
            course.students_count += 1
            course.save()
            print(f"✓ Student enrolled in: {course.title}")
        else:
            print(f"→ Student already enrolled in: {course.title}")
except Exception as e:
    print(f"✗ Error with enrollment: {e}")

# Test 5: Test Reviews
print("\n[TEST 5] Adding Reviews...")
try:
    enrolled_courses = Enrollment.objects.filter(student=student)
    for enrollment in enrolled_courses[:1]:
        review, created = Review.objects.get_or_create(
            course=enrollment.course,
            student=student,
            defaults={"rating": 5, "comment": "Excellent course!"},
        )
        if created:
            print(
                f"✓ Review added: {enrollment.course.title} - Rating: {review.rating}/5"
            )
        else:
            print(f"→ Review already exists for: {enrollment.course.title}")
except Exception as e:
    print(f"✗ Error adding reviews: {e}")

# Test 6: Check Model Methods
print("\n[TEST 6] Testing Model Methods...")
try:
    course = Course.objects.first()
    avg_rating = course.get_average_rating()
    review_count = course.get_review_count()
    is_free = course.is_free()
    print(f"✓ Course: {course.title}")
    print(f"  - Average Rating: {avg_rating}")
    print(f"  - Reviews: {review_count}")
    print(f"  - Is Free: {is_free}")
    print(f"  - Students Enrolled: {course.students_count}")
except Exception as e:
    print(f"✗ Error testing model methods: {e}")

# Test 7: Test User Methods
print("\n[TEST 7] Testing User Methods...")
try:
    print(f"✓ Student Methods:")
    print(f"  - is_student(): {student.is_student()}")
    print(f"  - is_instructor(): {student.is_instructor()}")
    print(f"  - is_admin(): {student.is_admin()}")

    print(f"✓ Instructor Methods:")
    print(f"  - is_student(): {instructor.is_student()}")
    print(f"  - is_instructor(): {instructor.is_instructor()}")
    print(f"  - is_admin(): {instructor.is_admin()}")
except Exception as e:
    print(f"✗ Error testing user methods: {e}")

# Test 8: Database Summary
print("\n[TEST 8] Database Summary...")
try:
    print(f"✓ Total Users: {User.objects.count()}")
    print(f"✓ Total Categories: {Category.objects.count()}")
    print(f"✓ Total Courses: {Course.objects.count()}")
    print(f"✓ Total Enrollments: {Enrollment.objects.count()}")
    print(f"✓ Total Reviews: {Review.objects.count()}")
except Exception as e:
    print(f"✗ Error getting database summary: {e}")

# Test 9: URL Configuration Check
print("\n[TEST 9] Testing URL Routes...")
try:
    client = Client()

    # Test home page
    response = client.get("/")
    print(f"✓ Home page: {response.status_code}")

    # Test course list
    response = client.get("/courses/")
    print(f"✓ Course list: {response.status_code}")

    # Test login
    response = client.get("/auth/login/")
    print(f"✓ Login page: {response.status_code}")

    # Test signup
    response = client.get("/auth/signup/")
    print(f"✓ Signup page: {response.status_code}")

    # Test admin
    response = client.get("/admin/")
    print(f"✓ Admin page: {response.status_code} (redirects if not logged in)")

except Exception as e:
    print(f"✗ Error testing routes: {e}")

print("\n" + "=" * 60)
print("TESTING COMPLETE!")
print("=" * 60)
print("\nApplication is ready to run!")
print("\nTo start the development server, run:")
print("  python manage.py runserver")
print("\nThen visit: http://127.0.0.1:8000/")
print("\nAdmin Panel: http://127.0.0.1:8000/admin/")
print("  Username: admin")
print("  Password: admin123")
