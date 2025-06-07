from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = 'contacts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    contact_id : Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    