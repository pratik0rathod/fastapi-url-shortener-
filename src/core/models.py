from .database import Base
from sqlalchemy.orm import Mapped,mapped_column

class User(Base):
    __tablename__ = "User"
    id:Mapped[int] = mapped_column(primary_key=True)
    usernmae:Mapped[str] = mapped_column(unique=True)
    email:Mapped[str] = mapped_column(unique=True)
    password:Mapped[str]

    