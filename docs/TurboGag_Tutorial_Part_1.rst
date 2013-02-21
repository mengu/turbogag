TurboGag Tutorial
=================

Let's learn TurboGears by example. 

Since Reddit is already open sourced we are going to teach you how to build a 9gag clone with TurboGears. We are going to let our users share and like funny and interesting photos and videos. Our users will be able to signup via Facebook and vote the submissions. After you are done with this tutorial you will learn:

* Working with built-in authentication and authorization.
* Working with forms and validation.
* Using sessions
* Using TurboGears admin panel.
* Using SQLAlchemy.

By reading this tutorial, you hereby acknowledge you have a working TurboGears installation. It sounded like very enterprisey, didn't it? Fear not, installing TurboGears will only take a few minutes depending on your internet connection.

Requirements before installation
--------------------------------
You need Python 2.x and virtualenv in your system in order to install TurboGears.

    1. `Download Python <http://www.python.org/getit/>`_

    2. `Install Python Setuptools <http://pypi.python.org/pypi/setuptools#installation-instructions>`_
    
    3. `Install virtualenv <http://www.virtualenv.org/en/latest/>`_


Why virtualenv?
~~~~~~~~~~~~~~~
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
--------------------

There are many options for you to quickstart a TurboGears project as however you wish. For example, you can disable authentication for a project, or use Mako or Jinja for templating or generate just a single file application. For more information run the ``paster quickstart -h`` command.

For the TurboGag project, we are going to use Jinja templates and the built-in authentication and authorization. Let's generate our project.

.. code:: bash

    paster quickstart -a -j TurboGag
  
TurboGears is now generating a Python project named TurboGag with Jinja and authentication. 

Where to create the project?
----------------------------

As you remember from installing TurboGears, you have to create a virtual environment. You should run the command above in that virtual environment right after activating it. For example, /home/user/projects is a good directory to keep your projects and virtual environments.

The application skeleton
------------------------

Your layout of TurboGag application will be something like the following image. The skeleton should make sense to you since controllers directory is where you create your controller classes and the same applies for models and templates.

[Skeleton screenshot here]

Another good thing for us is that we generated an application with user authentication and authorization. This will help us build the TurboGag application a lot faster. We won't have to deal with logging the user in, checking their permissions, etc. The only thing we are going to do is building a user registration form.

Running the application
-----------------------
Before starting the work on the application, let's take a quick look at what the quickstarted application has done for us. Run the following command in order to serve the application.

.. code::python

    python setup.py develop
    paster serve development.ini

The first command will introduce your application as a package to Python library path so all your imports and access requests will work. The second command will start an HTTP server for you to browse your application. Yes, indeed TurboGears twitter-bootsrapped your application for you in advanced. You can enjoy what it has to offer you.

Setting up the database
-----------------------
Since TurboGears has full support for SQLAlchemy and SQLAlchemy supports almost every database server, this step is going to be *very easy* for you. TurboGears configuration files live in .ini files such as development.ini for development and production.ini for production. Open up your development.ini file and go to line 62. You will see the SQLAlchemy uri for SQLite. By default TurboGears provides you a skeleton for which all the stack is right there for you, waiting for you to do your magic. The line is like the following:

::

    sqlalchemy.url = sqlite:///%(here)s/devdata.db

We are more than fine to use SQLite for development purposes however If you want to use MySQL or PostgreSQL, please read `SQLAlchemy documentation page on database uris <http://docs.sqlalchemy.org/en/rel_0_8/core/engines.html#database-urls>`_.

Creating the models
-------------------
Before moving on making the application work in the browser, let's just create the models we are going to use. In TurboGag application we will have a Submission model, a User model, a Vote model and a Comment model. Luckily we have user model already generated for us.

.. code:: python

    # -*- coding: utf-8 -*-
    """Submission model module."""

    from sqlalchemy import Table, ForeignKey, Column
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



"Where do I add the models?" you wonder. Create a Python file called ``submission.py`` in ``turbogag/model`` directory and write the down the codes from above. I hear the next question that pops in your head. How do I generate my models and my database? TurboGears extensions for paster are very rich. You can generate your models and databases with:

.. code:: bash

    paster setup-app development.ini

But that did only generate authentication related tables? How come it didn't generate the other tables? It's because that we haven't imported our models from ``turbogag/model/submission.py`` to ``turbogag/model/__init__.py`` file. Let's do it.

.. code:: python

    # add to the end of model/__init__.py
    from turbogag.model.auth import User, Group, Permission
    from turbogag.model.submission import Channel, Submission, Vote, Comment

Now re-run the "paster setup-app development.ini" command and you will see a stream of SQLAlchemy CREATE TABLE output.


Preparements
------------
Before developing the application there will be somethings we are going modify at the beginning such as the stylesheet and the master template which our templates will extend.

Modifying the stylesheet
~~~~~~~~~~~~~~~~~~~~~~~~
This is going to be our stylesheet, open your ``turbogag/public/css/style.css`` and replace it.


.. code:: css
    body{background:#ddd;}.content{background:#fff;}.submission{padding:20px;}.submission-title{font-size:18px;margin-bottom:8px;}.submission-title a{color:#222;text-decoration:none;}.voting{margin-top:20px;}.votebox{background:#ddd;text-align:center;height:64px;cursor:pointer;width:100px;float:left;}.votebox:hover{background:#ccc;}.votebox img{padding-top:20px;}.vb-first{border-right:1px solid #eee;border-top-left-radius:5px;}.vb-sec{border-top-right-radius:5px;margin:0!important;}.sharing{border-top:1px solid #eee;border-bottom-right-radius:5px;border-bottom-left-radius:5px;background:#ddd;width:191px;padding:5px;}.comments,.likes{color:#999;font-size:11px;}.comments{background:url(/images/comment.png) no-repeat -1px;margin-left:-2px;display:inline-block;padding-left:30px;padding-bottom:5px;}.likes{background:url(/images/heart.png) no-repeat;margin-left:10px;display:inline-block;padding-left:30px;padding-bottom:5px;}.footer{margin-top:45px;border-top:1px solid #e5e5e5;padding:35px 0 36px;}.footer p{margin-bottom:0;color:#555;}.poster,.info{margin-bottom:8px;}

The master template
~~~~~~~~~~~~~~~~~~~
Open up your ``turbogag/templates/master.jinja`` and replace it with the following code:

.. code:: jinja

    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta charset="charset={{ response.charset }}"/>
        {% block master_head %}
        {% endblock %}
        <title>{% block master_title %}{% endblock %} - Powered by TurboGears</title>
        <link rel="stylesheet" type="text/css" media="screen" href="{{tg.url('/css/bootstrap.min.css')}}" />
        <link rel="stylesheet" type="text/css" media="screen" href="{{tg.url('/css/bootstrap-responsive.min.css')}}" />
        <link rel="stylesheet" type="text/css" media="screen" href="{{tg.url('/css/style.css')}}" />
        <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
        <script type="text/javascript" src="{{ tg.url('/javascript/bootstrap.js') }}"></script>
    </head>

    <body>
        <div class="container">

            <!-- Navbar -->
            <div class="navbar">
                <div class="navbar-inner">
                    <div class="container">
                        <a class="brand" href="#"><img src="{{tg.url('/images/turbogears_logo.png')}}" alt="TurboGears 2"/>turbogears2</a>
                        <ul class="nav nav-pills">
                            <li class="{% if page == 'index' %}active{% endif %}"><a href="{{ tg.url('/') }}">Welcome</a></li>
                            <li><a href="{{ tg.url('/about') }}" class="{% if page == 'about' %}active{% endif %}">About</a></li>
                            <li><a href="{{ tg.url('/data') }}" class="{% if page == 'data' %}active{% endif %}">Serving Data</a></li>
                            <li><a href="{{ tg.url('/environ') }}" class="{% if page == 'environ' %}active{% endif %}">WSGI Environment</a></li>
                        </ul>

                        {% if tg.auth_stack_enabled %}
                            <ul class="nav nav-pills pull-right">
                                {% if request.identity %}
                                    <li><a href="{{tg.url('/logout_handler')}}">Logout</a></li>
                                    <li><a href="{{tg.url('/admin')}}">Admin</a></li>
                                {% else %}
                                    <li><a href="{{tg.url('/login')}}">Login</a></li>
                                {% endif %}
                            </ul>
                        {% endif %}
                    </div>
                </div>
            </div>

            <!-- Flash messages -->

            {% with flash=tg.flash_obj.render('flash', use_js=False) %}
                <div class="row"><div class="span8 offset2">
                    {{ flash|safe }}
                </div></div>
            {% endwith %}

            {% block contents %}
            {% endblock %}

            <!-- End of main_content -->
            <footer class="footer hidden-tablet hidden-phone">
                <a class="pull-right" href="http://www.turbogears.org/2.2/"><img style="vertical-align:middle;" src="{{tg.url('/images/under_the_hood_blue.png')}}" alt="TurboGears 2" /></a>
                <p>Copyright &copy; {{ tmpl_context.project_name|default('TurboGears2') }} {{h.current_year()}}</p>
            </footer>
        </div>

        <div id="fb-root"></div>
        <script>(function(d, s, id) {
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) return;
        js = d.createElement(s); js.id = id;
        js.src = "//connect.facebook.net/en_US/all.js#xfbml=1";
        fjs.parentNode.insertBefore(js, fjs);
      }(document, 'script', 'facebook-jssdk'));</script>
    </body>
    </html>

Next, we are going to inspect the TurboGears shell.

Continue to Part 2.

