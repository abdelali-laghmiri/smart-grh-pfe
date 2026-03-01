from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session

from db.session import get_db
from apps.auth.schemas import LoginRequest,TokenResponse,UserResponse
from apps.auth.services import authenticate_user
from core.security import create_access_token

from apps.auth.dependencies import get_current_user,require_superuser


router = APIRouter(prefix="/auth",tags=["Auth"])


@router.post("/login",response_model=TokenResponse)
def login(request:LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, request.matricule, request.password)

    if not user :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid matricule or password",
        )
    acsses_thoken = create_access_token(
        data={
            "sub":user.matricule
        }
    )
    return TokenResponse(access_token=acsses_thoken)

@router.get("/me",response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return current_user

@router.get("/admin_only")
def admin_only(user = Depends(require_superuser)):
    return{"message":"welcomsuper user"}