# -*- coding: utf-8 -*-
"""Submission model module."""

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, Unicode, UnicodeText, DateTime, Boolean

from turbogag.model import DeclarativeBase, metadata, DBSession

class Channel(DeclarativeBase):
    __tablename__ = "channels"
    
    id = Column(Integer, primary_key=True)
    channel_name = Column(Unicode)


class Submission(DeclarativeBase):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("tg_user.user_id"))
    channel_id = Column(ForeignKey("channels.id"))
    content_type = Column(Unicode)
    title = Column(Unicode)
    image_url = Column(Unicode)
    video_url = Column(Unicode)
    is_active = Column(Boolean)

    user = relationship("User")


class Vote(DeclarativeBase):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True)
    submission_id = Column(ForeignKey("submissions.id"))
    user_id = Column(ForeignKey("tg_user.user_id"))
    dateline = Column(DateTime)


class Comment(DeclarativeBase):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    submission_id = Column(ForeignKey("submissions.id"))
    user_id = Column(ForeignKey("tg_user.user_id"))
    comment_text = Column(UnicodeText)
    dateline = Column(DateTime)
