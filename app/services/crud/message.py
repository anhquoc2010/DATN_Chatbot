from app.services.crud.base import CRUDBase
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageUpdate

CRUDMessage = CRUDBase[Message, MessageCreate, MessageUpdate]
crud_message = CRUDMessage(Message)