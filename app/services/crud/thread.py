from app.services.crud.base import CRUDBase
from app.models.thread import Thread
from app.schemas.thread import ThreadCreate, ThreadUpdate

CRUDThread = CRUDBase[Thread, ThreadCreate, ThreadUpdate]
crud_thread = CRUDThread(Thread)

