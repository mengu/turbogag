TurboGag Tutorial
===============

Let's learn TurboGears by example. 

Since Reddit is already open sourced we are going to teach you how to build a 9gag clone with TurboGears. After this tutorial you will learn:

* Working with built-in authentication and authorization.
* Working with forms and validation.
* Using sessions
* Using TurboGears admin panel.
* Using SQLAlchemy.

By reading this tutorial, you hereby acknowledge you have a working TurboGears installation.

Creating the project:
---------------

There are many options for you to quickstart a TurboGears project as however you wish. For example, you can disable authentication for a project, or use Mako or Jinja for templating or generate just a single file application. For more information run the `paster quickstart -h` command.

For the TurboGag project, we are going to use Jinja templates and the built-in authentication and authorization. Let's generate our project.

.. highlight::bash

    paster quickstart -a -j TurboGag
  
TurboGears is now generating a Python project named TurboGag with Jinja and authentication. 

Where to create the project?
---------------

As you remember from installing TurboGears, you have to create a virtual environment. You should run the command above in that virtual environment right after activating it. For example, /home/user/projects is a good directory to keep your projects and virtual environments.

The Application Skeleton
---------------

Your layout of TurboGag application will be something like the following image. The skeleton should make sense to you since controllers directory is where you create your controller classes and the same applies for models and templates.

[Skeleton screenshot here]

Another good thing for us is that we generated an application with user authentication and authorization. This will help us build the TurboGag application a lot faster. We won't have to deal with logging the user in, checking their permissions, etc. The only thing we are going to do is building a user registration form.

Running the application
------------
Before starting the work on the application, let's take a quick look at what the quickstarted application has done for us. Run the following command in order to serve the application.

::

    python setup.py develop
    paster serve development.ini

The first command will introduce your application as a package to Python library path so all your imports and access requests will work. The second command will start an HTTP server for you to browse your application. Yes, indeed TurboGears twitter-bootsrapped your application for you in advanced. You can enjoy what it has to offer you.

Setting up the database
---------------
Since TurboGears has full support for SQLAlchemy and SQLAlchemy supports almost every database server, this step is going to be *very easy* for you. TurboGears configuration files live in .ini files such as development.ini for development and production.ini for production. Open up your development.ini file and go to line 62. You will see the SQLAlchemy uri for SQLite. By default TurboGears provides you a skeleton for which all the stack is right there for you, waiting for you to do your magic. The line is like the following:

::

    sqlalchemy.url = sqlite:///%(here)s/devdata.db

We are more than fine to use SQLite for development purposes however If you want to use MySQL or PostgreSQL, please read `SQLAlchemy documentation page on database uris <http://docs.sqlalchemy.org/en/rel_0_8/core/engines.html#database-urls>`_.

Creating the models
---------------
Before moving on making the application work in the browser, let's just create the models we are going to use. In TurboGag application we will have a Submission model, a User model, a Vote model and a Comment model. Luckily we have user model already generated for us.

::

    # -*- coding: utf-8 -*-
    """Submission model module."""

    from sqlalchemy import Table, ForeignKey, Column
    from sqlalchemy.types import BigInteger, Unicode, UnicodeText, DateTime

    from turbogag.model import DeclarativeBase, metadata, DBSession
    
    class Channel(DeclarativeBase):
        __tablename__ = "channels"
        
        id = Column(BigInteger)
        channel_name = Column(Unicode)
        

    class Submission(DeclarativeBase):
        __tablename__ = "submissions"

        id = Column(BigInteger, primary_key=True)
        channel_id = Column(ForeignKey("channels.id"))
        title = Column(Unicode)
        content = Column(UnicodeText)
        


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


"Where do I add the models?" you wonder. Create a Python file called "submission.py" in turbogag/model directory and write the down the codes from above. I hear the next question that pops in your head. How do I generate my models and my database? TurboGears extensions for paster are very rich. You can generate your models and databases with:

::

    paster setup-app development.ini

But that did only generate authentication related tables? How come it didn't generate the other tables? It's because that we haven't imported our models from submission.py to model/__init__.py file. Let's do it.

::

    # add to the end of model/__init__.py
    from turbogag.model.auth import User, Group, Permission
    from turbogag.model.submission import Channel, Submission, Vote, Comment

Now re-run the "paster setup-app development.ini" command and you will see a stream of SQLAlchemy CREATE TABLE output.

Next, we are going to work on controllers and views. This is all for now. Take a deep breath and enjoy what you have accomplished so far.

Continue to Part 2.

