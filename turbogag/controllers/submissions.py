# -*- coding: utf-8 -*-
"""Submissions controller module"""

from tg import expose, redirect, validate, flash
from tg import predicates

from turbogag.lib.base import BaseController
from turbogag.model import DBSession, metadata
from turbogag.model.submission import Channel, Submission, Vote, Comment

class SubmissionsController(BaseController):

    @expose("turbogag.templates.submissions.new")
    def new(self):
        channels = DBSession.query(Channel).all()
        return dict(channels=channels)

    @expose()
    def create(self, title, content_type, image_url="", video_url=""):
        submission = Submission(title=title, content_type=content_type, image_url=image_url, video_url=video_url, is_active=False)
        DBSession.add(submission)
        DBSession.flush()
        flash("Your submission has been received. It will be approved in a short notice.")
        return redirect("/")

    @expose("turbogag.templates.submissions.edit")
    def edit(self, submission_id):
        pass

    @expose()
    def update(self, id, title, content, status):
        pass

    @expose()
    def delete(self, id):
        pass