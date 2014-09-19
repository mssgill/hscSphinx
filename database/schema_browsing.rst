.. _schema_browsing:

===================================
Schema Browsing of HSC SSP database
===================================

Online Schema Browser at NAOJ 
-----------------------------
Online schema browser is available on the NAOJ online 
`Schema Browser <https://hscdata.mtk.nao.ac.jp:4443/schema_browser2/schema_browser.html>`_. 
It shows column names, format in database, descriptions, value format, unit, DB key information and 
corresponding names in HSC pipeline. The target table can be switched by clicking the table names under the 
trees of the database schema, like 'ssp_s14a0_udeep_20140523a'(for UDEEP COSMOS), in the right panel.
Please read the top page of this `Schema Browser <https://hscdata.mtk.nao.ac.jp:4443/schema_browser2/schema_browser.html>`_ 
for the detail of usage. 

Scripts in hscDb package
------------------------
If the user installed HSC pipeline, hscDb package is available and there are 2 scripts for enabling 
users to browse the database table information. '**getHscTableName.py**' is for displaying all tables 
and views in the specified database schema. '**getHscTableInfo.py**' is for displaying the table schema 
of the specified database table, including index infromation/definition. 

Listing the table names::

    getHscTableName.py --dbname=database --dbhost=host_name or address --dbschema=schema_name
                -U kensaku -p password_for_kensaku_user

    ex) getHscTableName.py --dbname=dr_early --dbhost=192.168.0.1 --dbschema=ssp_s14a0_udeep_20140523a 
                -U kensaku -p password_for_kensaku_user

Listing the table schema::

    getHscTableInfo.py --dbname=database_name --dbhost=host_name or address --dbschema=schema_name 
                       -U kensaku -p password_for_kensaku_user table_name 

    ex) getHscTableInfo.py --dbname=dr_early --dbhost=192.168.0.1 --dbschema=ssp_s14a0_udeep_20140523a 
                       -U kensaku -p password_for_kensaku_user mosaic__deepcoadd 

Please ask the password of the user 'kensaku' to your database administrator. 

Using psql
----------
As already explained in :ref:`Basic PostgreSQL<postgres_intro>`, it is easy to use 'psql' command 
for accessing the database and '\dt+', '\dv+', '\di+' command for browsing information of tables, views 
and indeces. 
