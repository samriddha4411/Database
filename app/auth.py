from flask import Request
from app.models import *

def admin(request: Request):
    db = SessionLocal()
    user = db.query(User).filter(User.username == request.cookies.get("username")).first()
    db.close()
    
    # Checks if the user is admin or not
    if user.is_admin:
        return True
    else:
        return False