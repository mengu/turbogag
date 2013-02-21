TurboGag Tutorial
=================

The TurboGears shell
--------------------

.. code:: bash
    
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
~~~~~~~~~~~~~~~~~~~

.. code:: python

    # this will select all channels
    DBSession.query(Channel).all()

Select a channel with id 2
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    DBSession.query(Channel).filter(Channel.id == 2).one()
    # or
    DBSession.query(Channel).filter(id=2).first()


Order the channels
~~~~~~~~~~~~~~~~~~

.. code:: python

    # order channels by channel id descending
    DBSession.query(Channel).order_by(Channel.id.desc()).all()


Select only 3 channels
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    # select 3 channels ordered by channel names ascending
    DBSession.query(Channel).order_by(Channel.channel_name.asc()).limit(3).all()

Update a channel name
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    channel = DBSession.query(Channel).filter_by(id=1).one()
    channel.channel_name = "so cool"
    DBSession.add(channel)

Delete a channel
~~~~~~~~~~~~~~~~

.. code:: python

    DBSession.query(Channel).filter_by(id=6).delete()

No! That is not all you can do with SQLAlchemy. You can create many more complex queries with it. SQLAlchemy is a very very powerful tool. If you would like to play with it, I will glady wait. Go read some tutorials or try to create that SQL that you could not create with other ORMs. SQLAlchemy will not disappoint you.

Next, we are going to work on controllers and views. This is all for now. Take a deep breath and enjoy what you have accomplished so far.

Continue to Part 3.