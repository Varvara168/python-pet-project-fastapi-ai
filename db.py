from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

engine = create_engine(url="sqlite:///clients.db")

session = sessionmaker(engine)

class Base(DeclarativeBase): #родительский класс
    pass

class ChatRequests(Base):
    __tablename__ = "client_requests"
    id: Mapped[int] = mapped_column(primary_key=True)
    ip_address: Mapped[str] = mapped_column(index=True) #очень быстрый поиск
    promt: Mapped[str]
    response: Mapped[str]

def get_user_requests(ip_address: str) -> list[ChatRequests]:
    with session() as new_session: #контекст менеджер  позволяет автоматичпеески закрывать сессиии что б не перегружать
        query = select(ChatRequests).filter_by(ip_address=ip_address)
        result = new_session.execute(query)
        return result.scalars().all()
        #execute - выполнить


def add_request_data(ip_address: str, promt: str, response: str) -> None:
    with session() as new_session: #контекст менеджер  позволяет автоматичпеески закрывать сессиии что б не перегружать
        new_request = ChatRequests(
            ip_address=ip_address,
            promt=promt,
            response=response,

        )
        new_session.add(new_request)
        new_session.commit()
        #execute - выполнить