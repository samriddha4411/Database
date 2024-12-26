import os

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        'postgresql+psycopg2://postgres.bpafhufsceoblbyxeemf:hGCg19hjpG1ObNdY@aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require&supa=base-pooler.x'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security: Generate a secret key or load from an environment variable
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))

    # Additional configurations can be added here as needed

# import os

# class Config:
#     SQLALCHEMY_DATABASE_URI = os.getenv(
#         'DATABASE_URL', 
#         'postgresql+psycopg2://postgres.bpafhufsceoblbyxeemf:hGCg19hjpG1ObNdY@aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require&supa=base-pooler.x'
#     )
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = os.urandom(24)  # or another method to set a secret key

# import os

# class Config:
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgres://postgres.bpafhufsceoblbyxeemf:hGCg19hjpG1ObNdY@aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require&supa=base-pooler.x')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = os.urandom(24)  # or another method to set a secret key