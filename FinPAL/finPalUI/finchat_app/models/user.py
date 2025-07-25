from sqlalchemy import Column, String, TIMESTAMP, text, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext
import uuid

Base = declarative_base()
# Password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "agent"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password = Column(String)
    name = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))
    age = Column(Integer)
    designation = Column(String)
    salary = Column(Numeric)


    
    @classmethod
    def hash_password(cls, plain_password: str) -> str:
        """Hash the password before saving to the database."""
        return pwd_context.hash(plain_password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """Verify the hashed password."""
        return pwd_context.verify(plain_password, hashed_password)