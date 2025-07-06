from fastapi import APIRouter

from crud.chat_history_crud import ChatHistoryCrud
from crud.chat_session_crud import ChatSessionCrud
from models.chat_session_model import ChatSessionParams, ChatSessionResponse
from routers.base import success
from fastapi import HTTPException

router = APIRouter(
    prefix="/session",
    tags=["session"],
    responses={404: {"message": "您所访问的资源不存在！"}},
)

chat_session_crud = ChatSessionCrud()
chat_history_crud = ChatHistoryCrud()


@router.get("/list", response_model=ChatSessionResponse)
async def chat_session_list(user_name: str):
    results = chat_session_crud.list(user_name)
    return success(results)


@router.post("/add")
async def chat_session_add(params: ChatSessionParams):
    if not params.user_name:
        raise HTTPException(status_code=422, detail="user_name is required")
    results = chat_session_crud.save(params)
    return success(results)


@router.put("/update")
async def chat_session_update(params: ChatSessionParams):
    results = chat_session_crud.save(params)
    return success(results, "修改成功！")


@router.delete("/delete")
async def chat_session_delete(params: ChatSessionParams):
    chat_history_crud.delete_by_chat_session_id(params.id)
    chat_session_crud.delete(params.id)
    return success(None, "删除成功！")
