# -*- coding: utf-8 -*-
"""Submission model module."""

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import BigInteger, Unicode, UnicodeText, DateTime

from turbogag.model import DeclarativeBase, metadata, DBSession

class Channel(DeclarativeBase):
    __tablename__ = "channels"
    
    id = Column(BigInteger, primary_key=True)
    channel_name = Column(Unicode)


class Submission(DeclarativeBase):
    __tablename__ = "submissions"

    id = Column(BigInteger, primary_key=True)
    channel_id = Column(ForeignKey("channels.id"))
    content_type = Column(Unicode)
    title = Column(Unicode)
    image_url = Column(Unicode)
    video_url = Column(Unicode)


class Vote(DeclarativeBase):
    __tablename__ = "votes"

    id = Column(BigInteger, primary_key=True)
    submission_id = Column(ForeignKey("submissions.id"))
    user_id = Column(ForeignKey("tg_user.user_id"))
    dateline = Column(DateTime)


class Comment(DeclarativeBase):
    __tablename__ = "comments"

    id = Column(BigInteger, primary_key=True)
    submission_id = Column(ForeignKey("submissions.id"))
    user_id = Column(ForeignKey("tg_user.user_id"))
    comment_text = Column(UnicodeText)
    dateline = Column(DateTime)