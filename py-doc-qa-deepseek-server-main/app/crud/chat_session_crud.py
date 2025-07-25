from fastapi import HTTPException
from sqlmodel import Session, desc, select
from models.chat_session_model import ChatSession, ChatSessionParams, ChatSessionUpdate
import uuid
from .base import engine


class ChatSessionCrud:
    def save(self, data: ChatSessionParams):
        chat_session = ChatSessionUpdate(title=data.title)

        if data.id:
            with Session(engine) as session:
                db_update_session = session.get(ChatSession, data.id)
                if db_update_session.user_name != data.user_name:  # 使用data.user_name
                    raise HTTPException(status_code=403, detail="无权修改此会话记录。")
                chat_session = chat_session.model_dump(exclude_unset=True)
                db_update_session.sqlmodel_update(chat_session)
                session.add(db_update_session)
                session.commit()
                session.refresh(db_update_session)
                return db_update_session

        with Session(engine) as session:
            # 创建时使用data.user_id
            db_add_session = ChatSession(
                title=data.title,
                user_name=data.user_name
            )
            session.add(db_add_session)
            session.commit()
            session.refresh(db_add_session)
            return db_add_session

    def list(self, user_name: str):
        with Session(engine) as session:
            query = select(ChatSession).order_by(desc(ChatSession.date))
            if user_name:
                query = query.where(ChatSession.user_name == user_name)
            query = query.order_by(desc(ChatSession.date))
            chat_session_list = session.exec(query).all()
            return chat_session_list

    def delete(self, id: str):
        """删除会话记录"""
        with Session(engine) as session:
            db = session.get(ChatSession, id)
            if not db:
                raise HTTPException(status_code=500, detail="会话记录不存在。")
            

            session.delete(db)
            session.commit()
