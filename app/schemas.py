from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import date

# Student schemas
class StudentBase(BaseModel):
    name: str
    email: EmailStr  # Email validation

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True  # For SQLAlchemy 2.0 compatibility

# Course schemas
class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True  # For SQLAlchemy 2.0 compatibility

# Enrollment schemas
class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class Enrollment(EnrollmentBase):
    enrolled_on: date

    class Config:
        orm_mode = True
        from_attributes = True  # For SQLAlchemy 2.0 compatibility

# Extended schemas for relationships
class CourseWithoutStudents(Course):
    pass

class StudentWithCourses(Student):
    courses: List[CourseWithoutStudents] = []

    class Config:
        orm_mode = True
        from_attributes = True  # For SQLAlchemy 2.0 compatibility

class StudentWithoutCourses(Student):
    pass

class CourseWithStudents(Course):
    students: List[StudentWithoutCourses] = []

    class Config:
        orm_mode = True
        from_attributes = True  # For SQLAlchemy 2.0 compatibility
