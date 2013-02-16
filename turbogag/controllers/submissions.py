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
    def create(self, title, content):
        submission = Submission(title=title, content=content, is_active=False)
        DBSession.add(submission)
        DBSession.flush()
        return redirect("/submissions/%s" % submission.id)

    @expose("turbogag.templates.submissions.edit")
    def edit(self, submission_id):
        try:
            submission = DBSession.query(Submission).filter(Submission.id == submission_id).one()
            return dict(submission=submission)
        except:
            return redirect("/")

    @expose()
    def update(self, id, title, content, status):
        try:
            submission = DBSession.query(Submission).filter_by(id=id).one()
            submission.title = title
            submission.content = content
            submission.status = status
            DBSession.add(submission)
            DBSession.flush()
            return redirect("/submissions/%s" % id)

        except:
            return redirect("/")

    @expose()
    def delete(self, id):
        DBSession.query(Submission).filter_by(id=id).delete()
        return redirect("/")