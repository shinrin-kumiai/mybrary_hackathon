from sqlalchemy import Column, ForeignKey, Integer, String, Table, DateTime
from sqlalchemy.orm import relationship

from src.database.database import Base, engine


class Book(Base):
    """国立国会図書館APIから取得した本のデータを格納するテーブル

    Args:
        Base (<class 'sqlalchemy.orm.decl_api.DeclarativeMeta'>): imported from src.database.database
    """
    __tablename__ = "book"
    id = Column(String(length=36), primary_key=True)
    isbn = Column(String(length=30))
    jan = Column(String(length=30))
    title = Column(String(length=100))
    author = Column(String(length=50))
    publisher = Column(String(length=20))
    price = Column(Integer)
    language = Column(String(length=20))
    page_count = Column(Integer)
    size = Column(Integer)
    # publish_date = Column(Date)
    user_book = relationship("UserBook", back_populates="book")
    community_book = relationship("CommunityBook", back_populates="book")


class UserBook(Base):
    """ユーザーとそのユーザーが所有している本との紐づけを行うテーブル

    Args:
        Base (<class 'sqlalchemy.orm.decl_api.DeclarativeMeta'>): imported from src.database.database
    """
    __tablename__ = "user_book"
    id = Column(String(length=36), primary_key=True)
    user_id = Column(String(length=36), ForeignKey("user.id"))
    book_id = Column(String(length=36), ForeignKey("book.id"))
    book = relationship("Book", back_populates="user_book")
    user_book_state_log = relationship("UserBookStateLog", back_populates="user_book")
    user = relationship("User", back_populates="user_book")


class CommunityBook(Base):
    """コミュニティとそのコミュニティが所有している本との紐づけを行うテーブル

    Args:
        Base (<class 'sqlalchemy.orm.decl_api.DeclarativeMeta'>): imported from src.database.database
    """
    __tablename__ = "community_book"
    id = Column(String(length=36), primary_key=True)
    community_id = Column(String(length=36), ForeignKey("community.id"))
    book_id = Column(String(length=36), ForeignKey("book.id"))
    book = relationship("Book", back_populates="community_book")
    community_book_state_log = relationship("CommunityBookStateLog", back_populates="community_book")
    community = relationship("Community", back_populates="community_book")


class UserBookStateLog(Base):
    """ユーザー所有の本の状態ログを格納するテーブル

    Args:
        Base (<class 'sqlalchemy.orm.decl_api.DeclarativeMeta'>): imported from src.database.database
    """
    __tablename__ = "user_book_state_log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_book_id = Column(String(length=36), ForeignKey("user_book.id"))
    state_id = Column(Integer, ForeignKey("state.id"))
    register_date = Column(DateTime)
    user_book = relationship("UserBook", back_populates="user_book_state_log")
    state = relationship("State", back_populates="user_book_state_log")


class CommunityBookStateLog(Base):
    """community所有のbookの状態ログを格納するテーブル

    Args:
        Base (<class 'sqlalchemy.orm.decl_api.DeclarativeMeta'>): imported from src.database.database
    """
    __tablename__ = "community_book_state_log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    community_book_id = Column(String(length=36), ForeignKey("community_book.id"))
    state_id = Column(Integer, ForeignKey("state.id"))
    register_date = Column(DateTime)
    community_book = relationship("CommunityBook", back_populates="community_book_state_log")
    state = relationship("State", back_populates="community_book_state_log")


class State(Base):
    """state一覧テーブル

    Args:
        Base (<class 'sqlalchemy.orm.decl_api.DeclarativeMeta'>): imported from src.database.database
    """
    __tablename__ = "state"
    id = Column(Integer, primary_key=True, autoincrement=True)
    state = Column(String(length=10))
    user_book_state_log = relationship("UserBookStateLog", back_populates="state")
    community_book_state_log = relationship("CommunityBookStateLog", back_populates="state")


user_community_table = Table(
    "user_community",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("community_id", Integer, ForeignKey("community.id"))
)


class User(Base):
    """ユーザー情報を格納するテーブル

    Args:
        Base (<class 'sqlalchemy.orm.decl_api.DeclarativeMeta'>): imported from src.database.database
    """
    __tablename__ = "user"
    id = Column(String(length=36), primary_key=True)
    name = Column(String(length=25))
    mail_adress = Column(String(length=100))
    user_book = relationship("UserBook", back_populates="user")
    community = relationship("Community", secondary=user_community_table, back_populates="user")


class Community(Base):
    """コミュニティ情報を格納するテーブル

    Args:
        Base (<class 'sqlalchemy.orm.decl_api.DeclarativeMeta'>): imported from src.database.database
    """
    __tablename__ = "community"
    id = Column(String(length=36), primary_key=True)
    name = Column(String(length=30))
    owner_id = Column(Integer)
    community_book = relationship("CommunityBook", back_populates="community")
    user = relationship("User", secondary=user_community_table, back_populates="community")


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)