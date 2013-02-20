# -*- coding: utf-8 -*-
"""Submission model module."""

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.sql import func, select
from sqlalchemy.orm import relationship 
from sqlalchemy.types import Integer, Unicode, UnicodeText, DateTime, Boolean

from turbogag.model import DeclarativeBase, metadata, DBSession
from turbogag.model.auth import User

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

    user = relationship("User", lazy="dynamic")
    comments = relationship("Comment", lazy="dynamic")
    votes = relationship("Vote", lazy="dynamic")

    @classmethod
    def list_submissions(self, offset=0, limit=10):
        comments_count_query = select([func.count(Comment.id)]).where(Comment.submission_id == Submission.id).label("comments_count")
        vote_count_query = select([func.count(Vote.id)]).where(Vote.submission_id == Submission.id).where(Vote.liked == True).label("votes_count")
        submissions = DBSession.query(Submission.id, Submission.title, Submission.content_type, Submission.image_url,
                            Submission.video_url, comments_count_query, vote_count_query).offset(offset).limit(limit).all()
        return submissions


class Vote(DeclarativeBase):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True)
    submission_id = Column(ForeignKey("submissions.id"))
    user_id = Column(ForeignKey("tg_user.user_id"))
    liked = Column(Boolean)
    dateline = Column(DateTime)


class Comment(DeclarativeBase):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    submission_id = Column(ForeignKey("submissions.id"))
    user_id = Column(ForeignKey("tg_user.user_id"))
    comment_text = Column(UnicodeText)
    dateline = Column(DateTime)
