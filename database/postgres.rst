
================
Basic PostgreSQL
================

* changing your password::

  > ALTER USER username WITH PASSWORD 'secret';

    
* see all 'slash' commands::

  > \?

* list databases::

  > \l
  > SELECT datname from pg_database;

* list schema in db::

  > \dn
  > SELECT setting FROM pg_settings WHERE name='search_path';

* set schema::

  > set search_path to myschema

* show tables::

  > \dt
  > \dt+
  > \dt myschema.*  # for different search path
  > SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
  
* show columns::

  > \d table
  > SELECT column_name FROM information_schema.columns WHERE table_name ='table';
  

