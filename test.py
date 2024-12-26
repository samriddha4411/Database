from sqlalchemy import create_engine

engine = create_engine(
    'postgresql+psycopg2://postgres.bpafhufsceoblbyxeemf:hGCg19hjpG1ObNdY@aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require'
)
try:
    connection = engine.connect()
    print("Connection successful!")
    connection.close()
except Exception as e:
    print(f"Connection failed: {e}")
