from typing import Any, Dict
import inflection
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return inflection.underscore(cls.__name__)

    def dict(self) -> Dict[str, Any]:
        return {c.key: getattr(self, c.key, None) for c in inspect(self).mapper.column_attrs}
