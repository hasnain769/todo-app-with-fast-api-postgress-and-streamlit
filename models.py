from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'Users'
    uid:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(nullable=False)
    email:Mapped[str] = mapped_column(nullable=False)
    password:Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"<Program {self.name}>"

class Todos(Base):
    __tablename__ = 'Todos'
    todo_id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(nullable=False)
    description:Mapped[str] = mapped_column(nullable=False)
    uid:Mapped[int] = mapped_column(ForeignKey('Users.uid',ondelete='CASCADE'))

    def __repr__(self) -> str:
        return f"<Program {self.name}>"

