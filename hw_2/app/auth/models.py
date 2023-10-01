from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    hpasswd: Mapped[str]
    email: Mapped[str]
