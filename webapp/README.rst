===============================
Horaires Train Flask App
===============================

Serveur de parametrage pour appli horaires


Quickstart
----------

First, set your app's secret key as an environment variable. For example,
add the following to ``.bashrc`` or ``.bash_profile``.

.. code-block:: bash

    export HORAIRESFLASKAPP_SECRET='something-really-secret'


The very first requirement is that you have python3.5 installed and pip 
utility pointing to this version

If you don't already have it install virtualenv ::
. If python3.5 is contained within anaconda run the following command ::
    conda install virtualenv
. Else run the following command ::
    pip install virtualenv

Get the source code of the project ::
    git clone https://github.com/vilcenzo/horairesflaskapp

Then create a virtualenv for this project ::
    cd horairesflaskapp/webapp
    virtualenv - p /path/to/your/python3.5/binary proj_python_env

Now activate your virtual environment ::
    source set_env.sh

Then install the required packages ::
    pip install -r requirements/dev.txt

Now initialize the database ::
    ./init_db.sh

You are ready to go now ::
    ./run.sh


Regular use
-----------

Once your environment is installed, to start the server ::
    cd horairesflaskapp/webapp
    source set_env.sh
    ./run.sh


Deployment
----------

In your production environment, make sure the ``FLASK_DEBUG`` environment
variable is unset or is set to ``0``, so that ``ProdConfig`` is used.


Shell
-----

To open the interactive shell, run ::

    flask shell

By default, you will have access to the flask ``app``.


Running Tests
-------------

To run all tests, run ::

    flask test


Migrations
----------

Whenever a database migration needs to be made. Run the following commands ::

    flask db migrate

This will generate a new migration script. Then run ::

    flask db upgrade

To apply the migration.

For a full migration command reference, run ``flask db --help``.
