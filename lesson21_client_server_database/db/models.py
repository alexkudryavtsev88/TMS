from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(6), nullable=False)
    nationality = Column(String, nullable=True)
    posts = relationship(
        "Post",
        backref="user",
        passive_deletes=True,
        lazy="joined",  # used for automatic join 'users' and 'posts' tables
        innerjoin=True
    )
    comments = relationship("Comment", backref="user", passive_deletes=True)
    likes = relationship("Like", backref="user", passive_deletes=True)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id},"
            f" name={self.name},"
            f" age={self.age},"
            f" gender={self.gender},"
            f" nationality={self.nationality}"
            f")"
        )


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(20), nullable=False)
    description = Column(String(100), nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    comments = relationship("Comment", passive_deletes=True, lazy="joined", order_by="Comment.id.asc()")
    likes = relationship("Like", passive_deletes=True, lazy="joined")

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id},"
            f" title={self.title},"
            f" description={self.description},"
            f" user_id={self.user_id}"
            f")"
        )


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}" f"(id={self.id}," f" title={self.title}" f")"
        )


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False
    )
