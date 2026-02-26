from sqlalchemy.orm import Session
from passlib.context import CryptContext

# import the User and UserRole models
from .models import User,UserRole

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_users_by_role(db: Session, role: UserRole):
    users = db.query(User).filter(User.role == role).all() 
    return users

def get_password_hash(password)-> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(
        db : Session,
        matricule: str,
        password: str,
        role: UserRole = UserRole.USER
        ):
    
    if role == UserRole.SUPERUSER:
        if get_users_by_role(db, UserRole.SUPERUSER):
            raise ValueError("A superuser already exists.")
    if db.query(User).filter(User.matricule == matricule).first():
        raise ValueError("A user with this matricule already exists.")
    hashed_password = get_password_hash(password)
    db_user = User(
        matricule=matricule,
        hashed_password=hashed_password,
        role=role,
        is_active=True,
        first_login=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, matricule: str, password: str):
    db_user = db.query(User).filter(User.matricule == matricule).first()
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user

