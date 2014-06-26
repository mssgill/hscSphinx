

========
Database
========

Below we provide a brief intoduction to PostgreSQL, with a few
examples for working with the HSC database.  If you're already
familiar with PostgreSQL, the basic info (connection, database,
schema, etc) to get going is posted just below the table of contents.


.. toctree::
   :maxdepth: 3

   database/postgres
   database/queries
   database/cloning

See also the NAOJ online `Schema Browser <https://hscdata.mtk.nao.ac.jp:4443/schema_browser/hsc/hsc_online_schema_tableonly.html>`_.

DB connection info::

   # This will not often change
   User: kensaku
   Pass: The HSC standard one (you probably typed it to see this webpage)
   Port: 5432
   Host: hscdb.ipmu.jp

   # These will change with each new data release
   Database: dr_early
   Schemas:
       ssp_s14a0_wide_20140523a
       ssp_s14a0_udeep_20140523a

