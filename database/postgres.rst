
.. _postgres_intro:

================
Basic PostgreSQL
================

Getting Started
---------------

The PostgreSQL server at IPMU is being served from hscdb.ipmu.jp on
port 5432 (the standard port for PostgreSQL).  To connect to the
database, you'll need to have the ``psql`` client installed on your
machine.  Mac OSX has this available on macports and homebrew, and
Redhat based distributions (CentOS) have special yum installation
which requires specifying a special yum repository (see `here
<http://yum.postgresql.org/>`_).  Once you have ``psql`` installed,
you can connect to the database using the following::

   $ psql -h hscdb.ipmu.jp -U kensaku -d dr_early -p 5432

   # -h is the host
   # -U is the read-only user 'kensaku' (means 'search' in Japanese)
   # -d is the database name
   # -p is the port
   
..
   If you're logging in using your own account, you can change your password with the following command::

   > ALTER USER username WITH PASSWORD 'secret';

   .. warning:: Do not ever change the password while logged in as user ``kensaku``.
  

There is a default read-only user available on the database system.
The user ``kensaku`` (means 'search' or 'lookup' in Japanese) can be
accessed using the standard HSC login information.

Help
^^^^

The navigation, and display commands in postgreSQL are called meta-commands and start with a ``\`` (backslash).  To see a list of all such 'slash' commands::

  > \?

To get help on a given command, ``\h`` will show the syntax.  E.g. for the ``SELECT`` command::

  > \h SELECT

Without a command, ``\h`` will show a list of all commands for which ``\h`` help is available.


Displaying Info about the Database, Schema, and Tables
------------------------------------------------------
  
* List databases on the current database system (it's a small 'L')::

    > \l

* Connect to a specific database, e.g. the database called ``dr_early``::

    > \c dr_early

* See which database you're connected to::

    > SELECT current_database();
    
* List the schema in a database::

    > \dn

* Set a schema to be the default (in this example ... the early wide data ::

    > set search_path to ssp_s14a0_wide_20140523a;

    
* Describe tables in the current database and schema (assuming you set ``search_path`` already)::

    > \dt

    # add + for a bit more information
    > \dt+

    # specify the schema explicitly if different from current 'search_path' (the early udeep schema here)
    > \dt ssp_s14a0_udeep_20140523a.*
  
* Describe the columns in a table (e.g. table 'frame')::

    > \d frame

    
Shell commands
--------------

It rarely necessary, but occassionally you need to spawn a shell to run a bash command (e.g. ``ls``)::

    > \! ls

    
Querying
--------


SQL queries are written with a 'SELECT' statement.  We'll provide a
brief overview and then some examples, but there are a number of full
tutorials online. See for example `PostgreSQL Tutorial
<http://www.postgresqltutorial.com/postgresql-select/>`_.


Reserved words in SQL (of which PostgreSQL is a flavour) are
conventionally written in capital letters.  This helps make the
queries more reabable, but isn't a requirement.  So ``SELECT`` can be
written ``select``, and the psql client won't object.  In cases where
it helps for readability, the examples posted here will be spaced and
indented, but ``psql`` will happily process a single long command.
Thus, the following two queries are equivalent::

    > SELECT
         ra2000, decl2000, imag_psf
      FROM
         photoobj_mosaic__deepcoadd__iselect
      WHERE
         imag_psf < 23.0;

         
    > select ra2000, decl2000, imag_psf from photoobj_mosaic__deepcoadd__iselect where imag_psf < 23.0;


When you run a query, the output will be displayed on the terminal by
default.  When setting up a query, it's often a good idea to limit the
number of returned entries to e.g. 20 by appending ``LIMIT 20`` to
your query::

    > SELECT imag_psf FROM  photoobj_mosaic__deepcoadd__iselect LIMIT 20;

Saving a Query to a File
^^^^^^^^^^^^^^^^^^^^^^^^
    
In order to print output from a query to your local machine (the one
where you ran ``psql``), use ``\o file.dat`` to redirect the output to
``file.dat`` (it will be ascii text).  When your query is done, use
``\o`` with no argument to reset the output to the display.::


    > \o imag.dat
    > SELECT imag_psf FROM  photoobj_mosaic__deepcoadd__iselect LIMIT 20;
    > \o
    
      
Running a Query from a Script
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Your query can be written in a script outside the ``psql`` environment
(emacs has nice SQL text highlighting by default if you use the
``.sql`` file suffix).  You can then run the script through ``psql``
with the ``-f file.sql``::

    $ cat file.sql
    set search_path to ssp_s14a0_wide_20140523a;
    \o imag.dat
    SELECT imag_psf FROM  photoobj_mosaic__deepcoadd__iselect LIMIT 20;
    \o

    $ psql -h hscdb.ipmu.jp -U kensaku -d dr_early -p 5432 -f file.sql

If you omit the ``\o file.dat`` setting, the output will be sent to
``stdout`` (i.e. printed to your screen) and you can redirect it to a
file from there.
    
