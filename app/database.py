from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Log the DATABASE_URL (with password masked for security)
if DATABASE_URL:
    masked_url = DATABASE_URL
    if "@" in masked_url:
        parts = masked_url.split("@")
        if ":" in parts[0]:
            auth_parts = parts[0].split(":")
            masked_url = f"{auth_parts[0]}:****@{parts[1]}"
    logger.info(f"Database URL: {masked_url}")
else:
    logger.warning("No DATABASE_URL environment variable found")

# If no DATABASE_URL is provided, use SQLite as fallback
if not DATABASE_URL:
    logger.info("Using SQLite as fallback database")
    DATABASE_URL = "sqlite:///./student_course_api.db"

# Handle special case for Render PostgreSQL connection string
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    logger.info("Converting postgres:// to postgresql:// in DATABASE_URL")
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Connection retry logic
def get_engine(url, max_retries=5, retry_interval=2):
    logger.info(f"Initializing database engine with URL type: {url.split(':')[0]}")
    retries = 0
    last_exception = None
    
    while retries < max_retries:
        try:
            # For PostgreSQL, we need to specify SSL mode
            connect_args = {}
            if url.startswith("postgresql"):
                # Don't use connect_timeout for Render as it can take longer to connect
                connect_args = {
                    "sslmode": "require" if "render.com" in url else "prefer"
                }
            
            # For SQLite, we need check_same_thread=False
            if url.startswith("sqlite"):
                connect_args = {"check_same_thread": False}
            
            logger.info(f"Creating engine with connect_args: {connect_args}")
            
            engine = create_engine(
                url,
                pool_pre_ping=True,  # Test connections before using them
                pool_recycle=300,    # Recycle connections every 5 minutes
                pool_size=5,         # Smaller pool size for Render's free tier
                max_overflow=10,     # Fewer overflow connections
                connect_args=connect_args
            )
            
            # Test the connection with a simple query using text()
            logger.info("Testing database connection...")
            with engine.connect() as conn:
                # Use text() to create an executable SQL expression
                result = conn.execute(text("SELECT 1"))
                logger.info(f"Connection test result: {result.scalar()}")
            
            logger.info("✅ Database connection successful")
            return engine
        except Exception as e:
            last_exception = e
            retries += 1
            logger.error(f"Database connection attempt {retries} failed: {str(e)}")
            if retries < max_retries:
                logger.info(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
            else:
                logger.error(f"Max retries reached. Could not connect to the database.")
                # Instead of raising, we'll return None and handle it in main.py
                return None

# Create engine with retry logic
try:
    engine = get_engine(DATABASE_URL)
    if engine is None:
        logger.warning("Failed to connect to primary database, using SQLite fallback")
        # Use SQLite as fallback if PostgreSQL connection fails
        engine = create_engine("sqlite:///./fallback.db", connect_args={"check_same_thread": False})
except Exception as e:
    logger.error(f"Error creating database engine: {e}")
    # Use SQLite as fallback
    logger.warning("Using SQLite fallback due to error")
    engine = create_engine("sqlite:///./fallback.db", connect_args={"check_same_thread": False})

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
