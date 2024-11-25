import uuid
from dataclasses import dataclass

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.core.db.base_class import Base


@dataclass
class User(Base):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column()
    full_name: Mapped[str | None] = mapped_column(default=None)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_member: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=False)
    hashed_password: Mapped[str] = mapped_column()

    # person_id: Mapped[int] = mapped_column(ForeignKey("person.id"))
    # person: Mapped[app.directory.models.Person] = relationship(foreign_keys=person_id)

    # def model_validate():
    #     return
