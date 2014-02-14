This tutorial walks you through the steps of creating a 9gag clone in Turbogears.

Installation and Setup
======================

Install ``turbogag`` using the setup.py script::

    $ cd turbogag
    $ python setup.py install

Create the project database for any model classes defined::

    $ paster setup-app development.ini

Start the paste http server::

    $ paster serve development.ini

While developing you may want the server to reload after changes in package files (or its dependencies) are saved. This can be achieved easily by adding the --reload option::

    $ paster serve --reload development.ini

Then you are ready to go.
