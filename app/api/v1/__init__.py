from fastapi import APIRouter
from app.api.v1.message import router as message_router
from app.api.v1.thread import router as thread_router
from app.api.v1.chat import router as chat_router
from app.api.v1.organizations import router as organizations_router

router = APIRouter(prefix="/v1")

router.include_router(message_router)
router.include_router(thread_router)
router.include_router(chat_router)
router.include_router(organizations_router)
