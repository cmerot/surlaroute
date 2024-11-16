from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlmodel.main import default_registry


class Base(DeclarativeBase):
    __name__: str  # type: ignore
    registry = default_registry

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
