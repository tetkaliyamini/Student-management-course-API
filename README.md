# Student Course Management API

A RESTful API for managing students and their enrolled courses built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- Create and manage students
- Create and manage courses
- Enroll students in courses
- View student details with enrolled courses
- View course details with enrolled students
- Email validation
- Pagination for list responses
- Unit tests with pytest

## Tech Stack

- FastAPI: Modern, fast web framework for building APIs
- Pydantic: Data validation and settings management
- SQLAlchemy: SQL toolkit and ORM
- PostgreSQL: Production database (SQLite for development/testing)
- Alembic: Database migration tool
- pytest: Testing framework


## Installation

1. Clone the repository:

2. Create and activate a virtual environment:

3. Install dependencies:
pip install -r requirements.txt

4. Configure the database:
   - For SQLite (development/testing): No additional configuration needed
   - For PostgreSQL (production):
     - Install PostgreSQL
     - Create a database
     - Update the database URL in `app/database.py` and `alembic.ini`

5. Run database migrations:
    alembic revision --autogenerate -m "Initial migration"
    alembic upgrade head


## Running the Application

Start the FastAPI server:
  uvicorn app.main:app --reload
The API will be available at http://127.0.0.1:8000

## API Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

- `POST /students/`: Create a student
- `GET /students/{id}`: Get student details with list of enrolled courses
- `GET /students/`: List all students (with pagination)
- `POST /courses/`: Create a course
- `GET /courses/{id}`: Get course details with list of enrolled students
- `GET /courses/`: List all courses (with pagination)
- `POST /enroll/`: Enroll a student in a course
- `GET /enrollments/`: List all enrollments (with pagination)

## Running Tests

Run the test suite:
pytest

## Live API: https://student-management-course-api.onrender.com
## Using PostgreSQL in Production

To use PostgreSQL in production:

1. Uncomment the PostgreSQL database URL in `app/database.py`
2. Update the connection details with your PostgreSQL credentials
3. Install the PostgreSQL driver by uncommenting `psycopg2-binary` in `requirements.txt`
4. Update the database URL in `alembic.ini`


