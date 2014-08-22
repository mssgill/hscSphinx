.. _schema_browsing:

===================================
Schema Browsing of HSC SSP database
===================================

Online Schema Browser at NAOJ 
-----------------------------
Online schema browser is available on the NAOJ online 
`Schema Browser <https://hscdata.mtk.nao.ac.jp:4443/schema_browser/hsc/hsc_online_schema_tableonly.html>`_. 
It shows column names, format in database, descriptions, value format, unit, DB key information and 
corresponding names in HSC pipeline. The target table can be switched by clicking the tabs on upper side. 
Tabs with light blue color are for tables of image meta data, and green ones for catalog tables. 
User can do the search on the table by clicking the 'magnify glass' mark at the lower left corner, 
and also do reloading and setting the page size to be displayed. 

.. warning::

     * Current schema browser is not compatible with some types of web browser softwares. 
       We've confirmed the functionality with the following sets of browsers/OS in the development. 

          ======= =======
          OS      Browser
          ======= =======
          Linux   Firefox
          Linux   Chrome
          MacOS   Safari
          MacOS   Chrome
          MacOS   Firefox
          Windows Firefox
          Windows Chrome
          ======= =======

       Microsoft IE is not good for the use currently.

     * The loading is a little too slow.. We're planning to improve the speed of browsing in the next release. 
    
 
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


