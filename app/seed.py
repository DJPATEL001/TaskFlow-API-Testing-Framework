from datetime import datetime, timedelta
from app.database import engine, Base, SessionLocal
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.services.auth_service import hash_password


def seed_database():
    print("Initializing Database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        print("Seeding Users...")
        admin = User(
            name="System Admin",
            email="admin@example.com",
            password_hash=hash_password("Admin@12345"),
            role="admin",
        )
        qauser = User(
            name="QA Tester",
            email="qauser@example.com",
            password_hash=hash_password("Test@12345"),
            role="user",
        )
        devuser = User(
            name="Developer One",
            email="devuser@example.com",
            password_hash=hash_password("Dev@12345"),
            role="user",
        )

        db.add_all([admin, qauser, devuser])
        db.commit()

        # Refresh to get generated IDs
        db.refresh(admin)
        db.refresh(qauser)
        db.refresh(devuser)

        print("Seeding Projects...")
        p1 = Project(
            name="TaskFlow Backend REST API",
            description="Core FastAPI service for task and project management.",
            status="active",
            owner_id=qauser.id,
        )
        p2 = Project(
            name="REST API Test Automation Framework",
            description="Pytest and Requests automated test suite for API verification.",
            status="active",
            owner_id=qauser.id,
        )
        p3 = Project(
            name="Customer Portal UI",
            description="React frontend application for end customers.",
            status="active",
            owner_id=devuser.id,
        )
        p4 = Project(
            name="Legacy Data Migration",
            description="Migration project from legacy MySQL database to modern architecture.",
            status="completed",
            owner_id=admin.id,
        )
        p5 = Project(
            name="Mobile App v1.0",
            description="React Native cross-platform mobile app project.",
            status="archived",
            owner_id=qauser.id,
        )

        db.add_all([p1, p2, p3, p4, p5])
        db.commit()

        for p in [p1, p2, p3, p4, p5]:
            db.refresh(p)

        print("Seeding Tasks...")
        now = datetime.utcnow()
        tasks_data = [
            # Tasks for Project 1
            Task(
                title="Design Auth Endpoints Schema",
                description="Create Pydantic models for register and login endpoints.",
                priority="high",
                status="completed",
                project_id=p1.id,
                assigned_to=qauser.id,
                due_date=now + timedelta(days=2),
            ),
            Task(
                title="Implement JWT Token Auth",
                description="Add PyJWT token generation and Bearer verification middleware.",
                priority="critical",
                status="completed",
                project_id=p1.id,
                assigned_to=qauser.id,
                due_date=now + timedelta(days=3),
            ),
            Task(
                title="Create Project CRUD Routes",
                description="Build GET, POST, PUT, DELETE endpoints for projects.",
                priority="high",
                status="in_progress",
                project_id=p1.id,
                assigned_to=devuser.id,
                due_date=now + timedelta(days=5),
            ),
            Task(
                title="Create Task Filtering & Pagination",
                description="Support status, priority, page, and limit query parameters.",
                priority="medium",
                status="todo",
                project_id=p1.id,
                assigned_to=devuser.id,
                due_date=now + timedelta(days=7),
            ),

            # Tasks for Project 2
            Task(
                title="Setup Pytest Test Environment",
                description="Configure conftest.py with base_url and auth fixtures.",
                priority="critical",
                status="completed",
                project_id=p2.id,
                assigned_to=qauser.id,
                due_date=now + timedelta(days=1),
            ),
            Task(
                title="Build Auth API Client Class",
                description="Implement AuthClient class methods for login and register.",
                priority="high",
                status="in_progress",
                project_id=p2.id,
                assigned_to=qauser.id,
                due_date=now + timedelta(days=3),
            ),
            Task(
                title="Write Task Filtering Automated Tests",
                description="Cover filtering by priority, status, and pagination.",
                priority="high",
                status="todo",
                project_id=p2.id,
                assigned_to=qauser.id,
                due_date=now + timedelta(days=6),
            ),
            Task(
                title="Implement Database Validation Helpers",
                description="Write db_helpers.py using SQLAlchemy for direct DB verification.",
                priority="medium",
                status="todo",
                project_id=p2.id,
                assigned_to=qauser.id,
                due_date=now + timedelta(days=8),
            ),

            # Tasks for Project 3
            Task(
                title="User Login Interface Component",
                description="Build React login form with input validation.",
                priority="high",
                status="completed",
                project_id=p3.id,
                assigned_to=devuser.id,
                due_date=now + timedelta(days=4),
            ),
            Task(
                title="Dashboard Overview Widgets",
                description="Render project metrics and total pending tasks.",
                priority="medium",
                status="in_progress",
                project_id=p3.id,
                assigned_to=devuser.id,
                due_date=now + timedelta(days=9),
            ),
            Task(
                title="Task Kanban Board View",
                description="Drag-and-drop task status board.",
                priority="low",
                status="todo",
                project_id=p3.id,
                assigned_to=devuser.id,
                due_date=now + timedelta(days=12),
            ),

            # Tasks for Project 4
            Task(
                title="Export Old Database Tables to CSV",
                description="Dump legacy user records for ETL pipeline.",
                priority="medium",
                status="completed",
                project_id=p4.id,
                assigned_to=admin.id,
                due_date=now - timedelta(days=10),
            ),
            Task(
                title="Validate Foreign Key Constraints",
                description="Ensure all task project_ids reference valid projects.",
                priority="critical",
                status="completed",
                project_id=p4.id,
                assigned_to=admin.id,
                due_date=now - timedelta(days=5),
            ),

            # Tasks for Project 5
            Task(
                title="Push Notification Service Integration",
                description="Setup FCM for mobile push alerts.",
                priority="low",
                status="cancelled",
                project_id=p5.id,
                assigned_to=devuser.id,
                due_date=now - timedelta(days=15),
            ),
            Task(
                title="Offline SQLite Caching",
                description="Implement offline task storage on mobile device.",
                priority="medium",
                status="cancelled",
                project_id=p5.id,
                assigned_to=qauser.id,
                due_date=now - timedelta(days=20),
            ),
        ]

        db.add_all(tasks_data)
        db.commit()

        print(f"Database seeded successfully! Created {db.query(User).count()} Users, {db.query(Project).count()} Projects, {db.query(Task).count()} Tasks.")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
