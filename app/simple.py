"""
A simplified version of the application that can be used for testing.
This file doesn't depend on any database connection and can be used to verify
that the application can at least start up without errors.
"""

from fastapi import FastAPI

app = FastAPI(title="Student Course Management API - Simple Version")

@app.get("/")
def read_root():
    return {"message": "Simple API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "not connected"}
