from sqlalchemy import Column, Integer, String, DateTime, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import hashlib

Base = declarative_base()

# Table Design for users
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_admin = Column(Boolean, default=False)

# Table Design for API Keys
class Keys(Base):
    __tablename__ = 'keys'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    keys = Column(String, unique=True, nullable=False)

DATABASE_URL = "sqlite:///database.db"
BACKUPDB_URL = "sqlite:///.config/backup.db"
DATABASE_PASSWORD = "your_database_password_here"  # Replace with your actual database password

# Initialization for Local Database
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialization for Backup Database
engine = create_engine(BACKUPDB_URL)
Base.metadata.create_all(engine)
BackupSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def hash_password(password):
    # Hash the password three times using SHA-512
    for _ in range(3):
        password = hashlib.sha512(password.encode()).hexdigest()
    return password