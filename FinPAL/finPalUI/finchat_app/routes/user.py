


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from schema.user import UserCreate, UserLogin
from utils.db_sessions import SessionLocal

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create User Endpoint
@router.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if the email already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash the password before storing
        hashed_password = User.hash_password(user.password)

        # Create the new user
        new_user = User(
            email=user.email,
            name=user.name,
            age=user.age,
            designation=user.designation,
            salary=user.salary,
            password=hashed_password  # Store the hashed password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "id": new_user.id,
            "email": new_user.email,
            "name": new_user.name
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Login Endpoint
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Query the user by email
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify the password
    if not User.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    # If login is successful, return basic user info
    return {
        "id": db_user.id,
        "email": db_user.email,
        "name": db_user.name
    }
