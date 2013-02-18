TurboGag Tutorial
===============

Let's learn TurboGears by example. 

Since Reddit is already open sourced we are going to teach you how to build a 9gag clone with TurboGears. We are going to let our users share and like funny and interesting photos and videos. Our users will be able to signup via Facebook and vote the submissions. After you are done with this tutorial you will learn:

* Working with built-in authentication and authorization.
* Working with forms and validation.
* Using sessions
* Using TurboGears admin panel.
* Using SQLAlchemy.

By reading this tutorial, you hereby acknowledge you have a working TurboGears installation. It sounded like very enterprisey, didn't it? Fear not, installing TurboGears will only take a few minutes depending on your internet connection.

Requirements before installation
---------------
You need Python 2.x and virtualenv in your system in order to install TurboGears.

    1. `Download Python <http://www.python.org/getit/>`_

    2. `Install Python Setuptools <http://pypi.python.org/pypi/setuptools#installation-instructions>`_
    
    3. `Install virtualenv <http://www.virtualenv.org/en/latest/>`_


Why virtualenv?
~~~~~~~~~~~~~~~~~~~~~~
Often it's the case that the Python packages in your system path might clash. Let's say a package called X has a dependency Y. Another package called Z depends on Y as well but to a newer version of Y. When you install the newer Y, the library X stops working because Y has a change that breaks it. In order to prevent this, you create a virtual environment which only cares about the Python packages in itself and not the system path. This way it prevents your Python packages clashing and let them work in a harmony you create.


Now, let's install TurboGears. We are going to install the latest stable version of TurboGears which is 2.2.2 right now.

.. code:: bash

    # install setuptools
    sudo apt-get install python-setuptools
    # install virtualenv
    sudo easy_install virtualenv
    cd ~/projects
    virtualenv --no-site-packages tg2-env
    cd tg2-env
    source bin/activate
    easy_install -i http://tg.gy/current tg.devtools

We are installing TurboGears from the index http://tg.gy/current which has all the TurboGears dependencies with their specific and working versions. It is important that we are specifying the index, otherwise it would install a newer version of any dependency which might not be working with TurboGears.

Creating the project
---------------

There are many options for you to quickstart a TurboGears project as however you wish. For example, you can disable authentication for a project, or use Mako or Jinja for templating or generate just a single file application. For more information run the ``paster quickstart -h`` command.

For the TurboGag project, we are going to use Jinja templates and the built-in authentication and authorization. Let's generate our project.

.. code:: bash

    paster quickstart -a -j TurboGag
  
TurboGears is now generating a Python project named TurboGag with Jinja and authentication. 

Where to create the project?
---------------

As you remember from installing TurboGears, you have to create a virtual environment. You should run the command above in that virtual environment right after activating it. For example, /home/user/projects is a good directory to keep your projects and virtual environments.

The application skeleton
---------------

Your layout of TurboGag application will be something like the following image. The skeleton should make sense to you since controllers directory is where you create your controller classes and the same applies for models and templates.

[Skeleton screenshot here]

Another good thing for us is that we generated an application with user authentication and authorization. This will help us build the TurboGag application a lot faster. We won't have to deal with logging the user in, checking their permissions, etc. The only thing we are going to do is building a user registration form.

Running the application
------------
Before starting the work on the application, let's take a quick look at what the quickstarted application has done for us. Run the following command in order to serve the application.

.. code::python

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

.. code::python

    # -*- coding: utf-8 -*-
    """Submission model module."""

    from sqlalchemy import Table, ForeignKey, Column
    from sqlalchemy.types import Integer, Unicode, UnicodeText, DateTime, Boolean

    from turbogag.model import DeclarativeBase, metadata, DBSession
    
    class Channel(DeclarativeBase):
        __tablename__ = "channels"
        
        id = Column(Integer, primary_key=True)
        channel_name = Column(Unicode)
        

    class Submission(DeclarativeBase):
        __tablename__ = "submissions"

        id = Column(Integer, primary_key=True)
        channel_id = Column(ForeignKey("channels.id"))
        content_type = Column(Unicode)
        title = Column(Unicode)
        image_url = Column(Unicode)
        video_url = Column(Unicode)
        is_active = Column(Boolean)
        

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


"Where do I add the models?" you wonder. Create a Python file called ``submission.py`` in ``turbogag/model`` directory and write the down the codes from above. I hear the next question that pops in your head. How do I generate my models and my database? TurboGears extensions for paster are very rich. You can generate your models and databases with:

.. code:: bash

    paster setup-app development.ini

But that did only generate authentication related tables? How come it didn't generate the other tables? It's because that we haven't imported our models from ``turbogag/model/submission.py`` to ``turbogag/model/__init__.py`` file. Let's do it.

.. code:: python

    # add to the end of model/__init__.py
    from turbogag.model.auth import User, Group, Permission
    from turbogag.model.submission import Channel, Submission, Vote, Comment

Now re-run the "paster setup-app development.ini" command and you will see a stream of SQLAlchemy CREATE TABLE output.

The TurboGears shell
---------------
::
    
    paster shell development.ini

This command lets you enter the TurboGears shell. Within this shell TurboGears starts a Python shell with your package included. Do you think it's time to insert some channels? Type the following into your shell.

.. code:: bash

    from turbogag.model import DBSession, Channel
    import transaction

    cool = Channel(channel_name="cool")
    cute = Channel(channel_name="cute")
    lol = Channel(channel_name="lol")
    want = Channel(channel_name="want")
    wtf = Channel(channel_name="wtf")
    DBSession.add_all([cool, cute, lol, want, wtf])
    DBSession.flush()
    transaction.commit()

This way we are creating our lovely channels. Would you like a taste of querying SQLAlchemy models? Yes, you would. You are dying to find out how this thing works. Let's just slow down. What would you want to learn? 

Select all channels
~~~~~~~~~~~~~~~

.. code:: python

    # this will select all channels
    DBSession.query(Channel).all()

Select a channel with id 2
~~~~~~~~~~~~~~

.. code:: python

    DBSession.query(Channel).filter(Channel.id == 2).one()
    # or
    DBSession.query(Channel).filter(id=2).first()


Order the channels
~~~~~~~~~~~~~~~

.. code:: python

    # order channels by channel id descending
    DBSession.query(Channel).order_by(Channel.id.desc()).all()


Select only 3 channels
~~~~~~~~~~~~~~~

.. code:: python

    # select 3 channels ordered by channel names ascending
    DBSession.query(Channel).order_by(Channel.channel_name.asc()).limit(3).all()

Update a channel name
~~~~~~~~~~~~~~~

.. code:: python

    channel = DBSession.query(Channel).filter_by(id=1).one()
    channel.channel_name = "so cool"
    DBSession.add(channel)

Delete a channel
~~~~~~~~~~~~~~~

.. code:: python

    DBSession.query(Channel).filter_by(id=6).delete()

No! That is not all you can do with SQLAlchemy. You can create many more complex queries with it. SQLAlchemy is a very very powerful tool. If you would like to play with it, I will glady wait. Go read some tutorials or try to create that SQL that you could not create with other ORMs. SQLAlchemy will not disappoint you.

Next, we are going to work on controllers and views. This is all for now. Take a deep breath and enjoy what you have accomplished so far.

Continue to Part 2.

