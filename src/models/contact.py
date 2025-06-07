from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Contact(Base):
    __tablename__ = 'contacts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    contact_id : Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    