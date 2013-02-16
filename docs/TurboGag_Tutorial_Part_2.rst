TurboGag Tutorial
===============

Letting users upload submissions
---------------
Now we are going to let users upload submissions and we are going to enjoy some reddit re-posts. TurboGears controllers are Python classes inheriting from a special class called BaseController. Giving it a meaningful name is important. For example, the Root Controller is the controller class responding to the calls of your requested url path starting with "/" right after your domain. For example http://turbogag.com/submissions automatically maps to a child controller class or a class method called submissions.

We are going to create a submissions controller but first let's decide what actions we are going to have in it. 

* Our users will be able to post submissions. (create)
* A user will be able to update his submission. (update)
* A manager/moderator of TurboGag will be able to approve, update or delete user submissions. (moderate)
* Users will be able to comment on submissions.


::

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

In the code above, we have created class methods named "new", "create", "edit", "update" and "destroy". This class methods will be available to the users in the form of http://turbogag.com/submissions/{method_name}


Embedding new controllers
---------------
If you tried accessing one of these pages via the browser, you will get a 404 error. In order to access those controllers, you have to introduce them to the RootController. Open your controllers/root.py file and add the following line as an attribute.

::

    # import the controller first
    from turbogag.controllers.submissions import SubmissionsController
    submissions = SubmissionsController()

Now if you re-visit http://127.0.0.1:8080/submissions/new you will be able to access this controller action. You will get an another error that we will fix in the next steps.


Something exposed comes this way
---------------
If you have used Ruby on Rails, Django, Pylons or Pyramid there is a question in your head right from the beginning. I know that. Been there, done that. Where do I set my routes? TurboGears does not have a routing mechanism. "Whoa sir, I'm afraid I cannot continue" you might think. No, not yet. TurboGears uses object dispatch which means every attribute in your RootController is a path of the url. Let's inspect the previous url: http://127.0.0.1:8080/submissions/new.

* You visit http://127.0.0.1:8080/submissions/new
* TurboGears looks at the RootController
* It looks for the submissions attribute in RootController
* If it does not find an attribute or a method named submissions, it returns 404.
* If it finds it TurboGears calls that attribute
* It looks for another attribute "new" in SubmissionsController
* It returns it.

This basically means that you don't need to setup any routing for your application. Yes, that's right, that is totally cool.

Creating templates
---------------
Now that we have our controllers working for us, we can start building our forms and templates and fix all those errors. 

