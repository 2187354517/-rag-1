from sqlmodel import select, Session
from models.user_model import User
import uuid
class UserCrud:
    """用户CRUD操作"""
    
    def get(self, session: Session, user_id: uuid.UUID):
        """获取单个用户"""
        return session.exec(select(User).where(User.id == user_id)).first()
    
    def get_all(self, session: Session):
        """获取所有用户"""
        return session.exec(select(User)).all()
    
    def create(self, session: Session, user_data: dict):
        """创建用户"""
        user = User(**user_data)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    
    def update(self, session: Session, user_id: uuid.UUID, user_data: dict):
        """更新用户"""
        user = self.get(session, user_id)
        if not user:
            return None
            
        for key, value in user_data.items():
            setattr(user, key, value)
            
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    
    def delete(self, session: Session, user_id: uuid.UUID):
        """删除用户"""
        user = self.get(session, user_id)
        if not user:
            return False
            
        session.delete(user)
        session.commit()
        return True