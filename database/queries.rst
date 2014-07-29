

.. _database_queries:

==================
HSC Query Examples
==================

If you haven't done so, please read through the :ref:`introduction to
PostgreSQL <postgres_intro>` to familiarize yourself with the basics.

See also the NAOJ online `Schema Browser <https://hscdata.mtk.nao.ac.jp:4443/schema_browser/hsc/hsc_online_schema_tableonly.html>`_.

Example 1
^^^^^^^^^
Download :download:`example1.sql`


.. literalinclude:: example1.sql
   :language: sql


Example 2
^^^^^^^^^

Download :download:`example2.sql`

.. literalinclude:: example2.sql
   :language: sql

Example 3
^^^^^^^^^

Download :download:`example3.sql`

.. literalinclude:: example3.sql
   :language: sql


Example 4
^^^^^^^^^

Download :download:`example4.sql`

.. literalinclude:: example4.sql
   :language: sql


Example 5
^^^^^^^^^

One of the example for searching high-z objects. Magnitude limits must be tuned to the data quality. 

Download :download:`example5.sql`

.. literalinclude:: example5.sql
   :language: sql

Example 6
^^^^^^^^^

Searching the objects around the specified sky coordinates with color constraints. 

Download :download:`example6.sql`

.. literalinclude:: example6.sql
   :language: sql

Example 7
^^^^^^^^^

Search the objects detected on a CCD image by forced measurement and get their sky coordinate 
based shape information.  

Download :download:`example7.sql`

.. literalinclude:: example7.sql
   :language: sql
