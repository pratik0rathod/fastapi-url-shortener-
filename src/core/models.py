from .database import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship,backref
from sqlalchemy import ForeignKey,func
from datetime import datetime,timedelta
from typing import Optional
from sqlalchemy import Enum
import enum

class UserEnum(enum.Enum):
    SUPER_USER = "SUPER USER"
    NORMAL_USER = "NORMAL USER"
    ADMIN = "ADMIN"
    POWER_USER = "POWER USER"


class User(Base):
    __tablename__ = "User"
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    username:Mapped[str] = mapped_column(unique=True)
    email:Mapped[str] = mapped_column(unique=True)
    password:Mapped[str]
    user_type = mapped_column(Enum(UserEnum),default=UserEnum.NORMAL_USER,nullable=True)

class ShortUrls(Base):
    __tablename__ = "short_urls"
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    url:Mapped[str] 
    alias:Mapped[str] = mapped_column(unique=True)
    total_clicks:Mapped[int] = mapped_column(default=0)
    created_on:Mapped[datetime] = mapped_column(default=func.now())
    expire_on:Mapped[Optional[timedelta]] 
    author:Mapped[int] = mapped_column(ForeignKey("User.id"))
    owner = relationship(User, backref=backref("short_urls",cascade="all,delete"))
