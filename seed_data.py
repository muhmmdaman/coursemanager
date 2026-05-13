"""
Seed data script for Course Hub
Creates 10+ categories and 100+ courses with realistic data
Run with: python manage.py shell < seed_data.py
"""

from django.contrib.auth import get_user_model
from courses.models import Category, Course, Enrollment, Review
from datetime import datetime, timedelta
import random

User = get_user_model()

print("🌱 Starting seed data creation...")

# Categories
categories_data = [
    ("Programming", "Learn programming languages and development"),
    ("Web Development", "Build modern web applications"),
    ("Mobile Development", "Develop iOS and Android apps"),
    ("Data Science", "Master data analysis and machine learning"),
    ("Cloud & DevOps", "AWS, Docker, Kubernetes, and more"),
    ("Artificial Intelligence", "AI, Machine Learning, and Deep Learning"),
    ("Cybersecurity", "Secure your systems and data"),
    ("Business & Entrepreneurship", "Start and grow your business"),
    ("Digital Marketing", "Social media, SEO, and content marketing"),
    ("UI/UX Design", "Create beautiful and intuitive designs"),
    ("Database Design", "SQL, NoSQL, and data modeling"),
    ("Game Development", "Create games with Unity and Unreal"),
]

print(f"✓ Creating {len(categories_data)} categories...")
categories = []
for name, description in categories_data:
    cat, created = Category.objects.get_or_create(
        name=name, defaults={"description": description}
    )
    categories.append(cat)
    if created:
        print(f"  + Created: {name}")

# Course data templates
course_templates = {
    "Programming": [
        ("Python for Beginners", "Learn Python from scratch", 25, 20),
        ("Advanced Python", "Master Python advanced concepts", 35, 50),
        ("Java Fundamentals", "Complete Java tutorial", 30, 25),
        ("JavaScript Essentials", "Learn JavaScript basics", 28, 22),
        ("C++ Programming", "Professional C++ development", 40, 60),
        ("Go Language Basics", "Introduction to Google Go", 22, 18),
        ("Rust Programming", "Modern systems programming", 32, 40),
        ("Ruby on Rails", "Full-stack web development", 36, 45),
        ("PHP Web Development", "Server-side web development", 26, 20),
        ("TypeScript Advanced", "Advanced TypeScript patterns", 30, 35),
    ],
    "Web Development": [
        ("React.js Mastery", "Build modern UI with React", 32, 55),
        ("Vue.js Complete Guide", "Full Vue.js tutorial", 28, 45),
        ("Angular Deep Dive", "Enterprise Angular development", 38, 60),
        ("HTML & CSS Pro", "Advanced HTML5 and CSS3", 24, 18),
        ("Responsive Web Design", "Mobile-first design approach", 25, 30),
        ("Web Performance Optimization", "Fast and efficient websites", 30, 40),
        ("REST API Design", "Build scalable APIs", 28, 35),
        ("GraphQL Fundamentals", "Learn GraphQL query language", 26, 32),
        ("WebSockets & Real-time", "Real-time applications", 29, 38),
        ("Progressive Web Apps", "Build offline-first apps", 27, 33),
    ],
    "Mobile Development": [
        ("iOS Development with Swift", "Create iOS apps", 35, 50),
        ("Android Development", "Build Android applications", 33, 48),
        ("React Native Mastery", "Cross-platform mobile apps", 32, 45),
        ("Flutter Development", "Build beautiful Flutter apps", 30, 42),
        ("Xamarin Development", "Cross-platform C#", 31, 44),
        ("Mobile Security", "Secure mobile applications", 28, 35),
        ("App Store Optimization", "Get your app discovered", 20, 15),
        ("Mobile UI Design", "Amazing mobile interfaces", 26, 30),
        ("Push Notifications", "Engage users effectively", 22, 25),
        ("Mobile Testing", "Comprehensive testing strategies", 24, 28),
    ],
    "Data Science": [
        ("Python for Data Analysis", "Pandas and NumPy", 30, 40),
        ("Machine Learning Basics", "ML fundamentals", 35, 50),
        ("Deep Learning with TensorFlow", "Neural networks", 40, 60),
        ("Pandas Masterclass", "Data manipulation", 28, 35),
        ("Data Visualization", "Create stunning visualizations", 26, 32),
        ("SQL for Data Analysis", "Advanced SQL queries", 25, 30),
        ("Statistical Analysis", "Foundation of statistics", 32, 45),
        ("Natural Language Processing", "NLP for text analysis", 38, 55),
        ("Computer Vision", "Image processing and recognition", 42, 65),
        ("Time Series Analysis", "Forecasting and prediction", 34, 50),
    ],
    "Cloud & DevOps": [
        ("AWS Essentials", "Amazon Web Services basics", 32, 45),
        ("Docker Fundamentals", "Containerized applications", 28, 38),
        ("Kubernetes Mastery", "Container orchestration", 36, 55),
        ("CI/CD Pipelines", "Continuous integration", 30, 40),
        ("Azure Cloud Platform", "Microsoft Azure services", 33, 48),
        ("Google Cloud Platform", "GCP fundamentals", 32, 46),
        ("Infrastructure as Code", "Terraform and Ansible", 31, 44),
        ("Monitoring and Logging", "Prometheus and ELK", 29, 38),
        ("GitLab and GitHub", "Version control mastery", 24, 30),
        ("Serverless Architecture", "Lambda and functions", 28, 36),
    ],
    "Artificial Intelligence": [
        ("AI Fundamentals", "Introduction to AI", 30, 35),
        ("Reinforcement Learning", "Advanced RL techniques", 40, 60),
        ("Neural Networks", "Deep learning basics", 36, 50),
        ("Chatbot Development", "Build intelligent bots", 28, 35),
        ("Computer Vision AI", "Vision systems", 38, 55),
        ("NLP Expertise", "Language understanding", 35, 50),
        ("Generative AI", "Creative AI models", 32, 45),
        ("AI Ethics", "Responsible AI development", 26, 30),
        ("AI in Healthcare", "Medical AI applications", 28, 38),
        ("Recommender Systems", "Personalization engines", 30, 42),
    ],
    "Cybersecurity": [
        ("Cybersecurity Basics", "Security fundamentals", 28, 32),
        ("Ethical Hacking", "Penetration testing", 40, 65),
        ("Network Security", "Secure networking", 32, 45),
        ("Cryptography", "Encryption and security", 35, 50),
        ("Web App Security", "Secure coding practices", 30, 40),
        ("Security Operations", "SOC and monitoring", 34, 50),
        ("Incident Response", "Handle security breaches", 32, 45),
        ("Cloud Security", "Secure cloud environments", 31, 44),
        ("Zero Trust Security", "Modern security model", 28, 38),
        ("GDPR Compliance", "Data protection laws", 22, 28),
    ],
    "Business & Entrepreneurship": [
        ("Startups 101", "Launch your startup", 26, 28),
        ("Business Strategy", "Strategic planning", 30, 35),
        ("Leadership Skills", "Become a great leader", 28, 32),
        ("Negotiation Mastery", "Win-win negotiations", 24, 26),
        ("Marketing Strategy", "Modern marketing", 29, 34),
        ("Financial Management", "Business finance", 32, 40),
        ("Brand Building", "Create strong brands", 27, 30),
        ("Sales Excellence", "Closing the deal", 28, 32),
        ("Project Management", "Lead successful projects", 30, 38),
        ("Customer Service", "Exceptional service", 24, 26),
    ],
    "Digital Marketing": [
        ("Facebook Advertising", "Social media ads", 20, 22),
        ("Google Analytics", "Track and analyze data", 22, 24),
        ("SEO Mastery", "Dominate search results", 26, 30),
        ("Content Marketing", "Compelling content", 25, 28),
        ("Email Marketing", "Effective email campaigns", 22, 24),
        ("Influencer Marketing", "Leverage influencers", 21, 23),
        ("Video Marketing", "Create viral videos", 24, 26),
        ("Growth Hacking", "Rapid growth techniques", 28, 32),
        ("Web Analytics", "Data-driven decisions", 23, 25),
        ("Marketing Automation", "Streamline marketing", 25, 28),
    ],
    "UI/UX Design": [
        ("UI Design Principles", "Beautiful interfaces", 26, 30),
        ("Figma Mastery", "Professional design tool", 24, 28),
        ("User Research", "Understand your users", 28, 32),
        ("Wireframing", "Effective wireframes", 22, 24),
        ("Prototyping", "Interactive prototypes", 25, 28),
        ("Design Systems", "Scalable design", 27, 32),
        ("Accessibility Design", "Inclusive design", 25, 28),
        ("Motion Design", "Animate your designs", 26, 30),
        ("3D Design Basics", "Introduction to 3D", 30, 35),
        ("Adobe XD Pro", "Advanced design tool", 25, 28),
    ],
    "Database Design": [
        ("SQL Fundamentals", "Database basics", 24, 28),
        ("Advanced SQL", "Complex queries", 28, 35),
        ("MySQL Mastery", "MySQL database", 26, 32),
        ("PostgreSQL Pro", "Advanced PostgreSQL", 28, 35),
        ("MongoDB No SQL", "Document databases", 26, 32),
        ("Database Performance", "Optimization techniques", 30, 40),
        ("Data Warehousing", "Big data systems", 35, 50),
        ("Redis Caching", "In-memory databases", 24, 30),
        ("Database Architecture", "Scalable databases", 32, 45),
        ("Backup & Recovery", "Data protection", 22, 26),
    ],
    "Game Development": [
        ("Unity Basics", "Game development fundamentals", 32, 45),
        ("Unreal Engine 5", "Professional gaming", 40, 65),
        ("Godot Engine", "Open source game engine", 28, 38),
        ("Game Design", "Design principles", 26, 30),
        ("3D Game Development", "Create 3D games", 35, 50),
        ("Game Physics", "Realistic physics", 30, 42),
        ("Game Audio", "Music and sound design", 22, 26),
        ("Multiplayer Games", "Networking", 32, 45),
        ("VR Game Development", "Virtual reality games", 36, 52),
        ("Game Publishing", "Publish your game", 20, 24),
    ],
}

# Create courses
print(f"\n✓ Creating 100+ courses...")
instructor = User.objects.filter(role="instructor").first()
if not instructor:
    instructor = User.objects.create_user(
        username="instructor1",
        email="instructor1@example.com",
        password="instructor123",
        role="instructor",
        first_name="John",
        last_name="Doe",
    )

course_count = 0
for category_name, courses in course_templates.items():
    category = Category.objects.get(name=category_name)
    for title, description, duration, price in courses:
        start_date = datetime.now() + timedelta(days=random.randint(1, 30))
        level = random.choice(["beginner", "intermediate", "advanced"])

        course, created = Course.objects.get_or_create(
            title=title,
            instructor=instructor,
            defaults={
                "description": description,
                "category": category,
                "price": price,
                "duration_hours": duration,
                "level": level,
                "start_date": start_date,
            },
        )
        if created:
            course_count += 1
            if course_count % 10 == 0:
                print(f"  + Created {course_count} courses...")

print(f"\n✅ Successfully created {course_count} courses!")
print(f"📊 Statistics:")
print(f"  - Categories: {Category.objects.count()}")
print(f"  - Courses: {Course.objects.count()}")
print(f"  - Instructors: {User.objects.filter(role='instructor').count()}")
print(f"  - Total Users: {User.objects.count()}")
print(f"\n🎉 Seed data creation complete!")
