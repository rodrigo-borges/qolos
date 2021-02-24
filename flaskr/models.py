from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


Base = declarative_base()


class User(Base):

	__tablename__ = "user"

	id = Column(Integer, primary_key=True)
	username = Column(String(255), nullable=False)
	password = Column(String(255), nullable=False)

	posts = relationship("Post", back_populates="author")

	def __repr__(self):
		return "<User(id={}, username={}, password={}...)>".format(
			self.id, self.username, self.password[:5])


class Post(Base):

	__tablename__ = "post"

	id = Column(Integer, primary_key=True)
	author_id = Column(Integer, ForeignKey("user.id"))
	created = Column(DateTime(timezone=True), server_default=func.now())
	title = Column(Text, nullable=False)
	body = Column(Text, nullable=False)

	author = relationship("User", back_populates="posts")

	def __repr__(self):
		return "<Post(id={}, author_id={}, created={}, title={}, body={}...)>".format(
			self.id, self.author_id, self.created, self.title, self.body[:10])