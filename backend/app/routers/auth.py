from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import uuid

from ..database import get_db
from ..models.employee import Employee, Department, SocialStyle
from ..config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    department: Department = Department.TECH
    position: str = ""
    social_style: SocialStyle = SocialStyle.PROFESSIONAL


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    employee: dict


def create_token(employee_id: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode(
        {"sub": employee_id, "exp": expire},
        settings.secret_key,
        algorithm=settings.algorithm,
    )


async def get_current_employee(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> Employee:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        employee_id: str = payload.get("sub")
        if not employee_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=401, detail="Employee not found")
    return employee


@router.post("/register", response_model=TokenResponse)
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Employee).where(Employee.email == req.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    employee = Employee(
        id=str(uuid.uuid4()),
        email=req.email,
        full_name=req.full_name,
        department=req.department,
        position=req.position,
        social_style=req.social_style,
        hashed_password=pwd_context.hash(req.password),
        bizcoins=100,
    )
    db.add(employee)
    await db.commit()
    await db.refresh(employee)

    token = create_token(employee.id)
    return {
        "access_token": token,
        "token_type": "bearer",
        "employee": _employee_dict(employee),
    }


@router.post("/token", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Employee).where(Employee.email == form_data.username))
    employee = result.scalar_one_or_none()
    if not employee or not pwd_context.verify(form_data.password, employee.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = create_token(employee.id)
    return {
        "access_token": token,
        "token_type": "bearer",
        "employee": _employee_dict(employee),
    }


@router.get("/me")
async def get_me(current_employee: Employee = Depends(get_current_employee)):
    return _employee_dict(current_employee)


def _employee_dict(e: Employee) -> dict:
    return {
        "id": e.id,
        "email": e.email,
        "full_name": e.full_name,
        "department": e.department,
        "position": e.position,
        "social_style": e.social_style,
        "bizcoins": e.bizcoins,
        "avatar_url": e.avatar_url,
        "is_admin": e.is_admin,
    }
