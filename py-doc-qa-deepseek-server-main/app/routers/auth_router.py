from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
import hashlib
import uuid
from pydantic import BaseModel
from models.user_model import User
from crud.base import get_session
from routers.base import success

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    id: str
    username: str
    password: str
    email: str

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"message": "您所访问的资源不存在！"}},
)

@router.post("/register")
async def register(user: RegisterRequest, session: Session = Depends(get_session)):
    """用户注册(接收JSON数据)"""
    # 检查用户ID是否已存在
    existing_user = session.exec(select(User).where(User.id == uuid.UUID(user.id))).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="用户ID已存在")
    
    # 检查用户名是否已存在
    existing_username = session.exec(select(User).where(User.username == user.username)).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 创建用户
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    new_user = User(
        id=uuid.UUID(user.id),
        username=user.username,
        password=hashed_password,
        email=user.email
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return success({
        "user_id": str(new_user.id),
        "username": new_user.username
    }, "注册成功")

@router.post("/login")
async def login(login_data: LoginRequest, session: Session = Depends(get_session)):
    """用户登录(接收JSON数据)"""
    user = session.exec(select(User).where(User.username == login_data.username)).first()
    if not user or hashlib.sha256(login_data.password.encode()).hexdigest() != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return success({
        "access_token": str(user.id),
        "token_type": "bearer",
        "username": user.username
    }, "登录成功")

@router.get("/users")
async def get_users(session: Session = Depends(get_session)):
    """获取所有用户"""
    users = user_crud.get_all(session)
    return success(users, "获取成功")

@router.get("/users/{user_id}")
async def get_user(user_id: str, session: Session = Depends(get_session)):
    """获取单个用户"""
    user = user_crud.get(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return success(user, "获取成功")

@router.put("/users/{user_id}")
async def update_user(user_id: str, user_data: dict, session: Session = Depends(get_session)):
    """更新用户"""
    user = user_crud.update(session, user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return success(user, "更新成功")

@router.delete("/users/{user_id}")
async def delete_user(user_id: str, session: Session = Depends(get_session)):
    """删除用户"""
    if not user_crud.delete(session, user_id):
        raise HTTPException(status_code=404, detail="用户不存在")
    return success(None, "删除成功")