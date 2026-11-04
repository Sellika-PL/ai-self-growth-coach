
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select

from app.db import get_session
from app.models import User
from app.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user_id,
    hash_password,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])


class SignupRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class AccessTokenResponse(BaseModel):
    access_token: str


class UserResponse(BaseModel):
    id: str
    email: str


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def signup(request: SignupRequest, session: Session = Depends(get_session)) -> TokenResponse:
    existing = session.exec(select(User).where(User.email == request.email)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = User(email=request.email, password_hash=hash_password(request.password))
    session.add(user)
    session.commit()
    session.refresh(user)

    user_id = str(user.id)
    return TokenResponse(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),
    )


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, session: Session = Depends(get_session)) -> TokenResponse:
    user = session.exec(select(User).where(User.email == request.email)).first()

    invalid_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
    )

    if not user or not verify_password(request.password, user.password_hash):
        raise invalid_credentials

    user_id = str(user.id)
    return TokenResponse(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),
    )


@router.post("/refresh", response_model=AccessTokenResponse)
def refresh(request: RefreshRequest) -> AccessTokenResponse:
    user_id = decode_token(request.refresh_token, expected_type="refresh")
    return AccessTokenResponse(access_token=create_access_token(user_id))


@router.get("/me", response_model=UserResponse)
def me(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
) -> UserResponse:
    user = session.get(User, uuid.UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return UserResponse(id=str(user.id), email=user.email)
