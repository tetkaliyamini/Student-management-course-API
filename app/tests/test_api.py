import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models import Student, Course, Enrollment

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)

@pytest.fixture(scope="function")
def setup_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after test
    Base.metadata.drop_all(bind=engine)

def test_create_student(setup_database):
    response = client.post(
        "/students/",
        json={"name": "John Doe", "email": "john@example.com"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert "id" in data

def test_create_course(setup_database):
    response = client.post(
        "/courses/",
        json={"title": "Python Programming", "description": "Learn Python basics"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Python Programming"
    assert data["description"] == "Learn Python basics"
    assert "id" in data

def test_enroll_student(setup_database):
    # Create a student
    student_response = client.post(
        "/students/",
        json={"name": "Jane Smith", "email": "jane@example.com"},
    )
    student_id = student_response.json()["id"]
    
    # Create a course
    course_response = client.post(
        "/courses/",
        json={"title": "Web Development", "description": "Learn web development"},
    )
    course_id = course_response.json()["id"]
    
    # Enroll student in course
    enroll_response = client.post(
        "/enroll/",
        json={"student_id": student_id, "course_id": course_id},
    )
    assert enroll_response.status_code == 201
    
    # Check if student is enrolled in course
    student_detail_response = client.get(f"/students/{student_id}")
    assert student_detail_response.status_code == 200
    student_data = student_detail_response.json()
    assert len(student_data["courses"]) == 1
    assert student_data["courses"][0]["title"] == "Web Development"

def test_get_course_with_students(setup_database):
    # Create students
    student1 = client.post(
        "/students/",
        json={"name": "Alice", "email": "alice@example.com"},
    ).json()
    
    student2 = client.post(
        "/students/",
        json={"name": "Bob", "email": "bob@example.com"},
    ).json()
    
    # Create course
    course = client.post(
        "/courses/",
        json={"title": "Data Science", "description": "Learn data science"},
    ).json()
    
    # Enroll students
    client.post(
        "/enroll/",
        json={"student_id": student1["id"], "course_id": course["id"]},
    )
    
    client.post(
        "/enroll/",
        json={"student_id": student2["id"], "course_id": course["id"]},
    )
    
    # Get course with students
    response = client.get(f"/courses/{course['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Data Science"
    assert len(data["students"]) == 2
    student_names = [student["name"] for student in data["students"]]
    assert "Alice" in student_names
    assert "Bob" in student_names
