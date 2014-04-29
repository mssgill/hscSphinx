
=====================
General Pipeline Info
=====================

There are a variety of things which are common to all tasks associated
with a processing run.  Some of the things are just basic terminology
that you'll need to communicate with developers, while others are of
more practical importance for actually running the pipeline code
effectively.


Reruns
------

The term ``rerun`` dates back to SDSS.  It simply refers to a single
processing run of a set of data performed with a specified version of
the reduction code, and a specific set of configuration parameters.
The assumption is that within a given 'rerun', the data have been
handled in a homogeneous way.


The dataId
----------

A 'dataId' is a unique identifier for a specific data input.  The two
forms you most likely need to familiarize yourself with are the
'visit','ccd' identifiers used to refer to a specific CCD in a
specific exposure (called a 'visit'); and 'tract','patch' identifiers
which refer to the coordinate system used in coadded images.  Other important keys in a dataId might include:

* field (name you gave your target in the FITS header 'OBJECT' entry)
* dateObs (the date of observation from the FITS header 'DATE-OBS' entry)
* filter  (again from the FITS header ... 'FILTER' entry)

In almost any pipeline command you can specify which data you wish to process with ``--id dataID``, e.g.::

    # run visit 1000, CCD 50
    $ hscProcessCcd.py /data/ --id visit=1000 ccd=50

    # run all the HSC-I data from M87 taken on Jan 15, 2015
    $ hscProcessCcd.py /data/ --id field=M87 filter=HSC-I dateObs=2015-01-15

    # run tract 0 patch 1,1  in HSC-I for a coadd (here you'll need the filter too)
    $ hscProcessCoadd.py /data/ --id tract=0 patch=1,1 filter=HSC-I

Only a few of the dataId components are ever needed to uniquely
specify a given data input or output.  The observatory will never
reuse the number assigned as a 'visit', so it's impossible to have the
same visit with a different filter or dateObs.  Once you specify the
visit, the values are almost all redundant.  This isn't true for
tracts and patches, though!  A tract,patch refers to a location on the
sky and can have multiple filters or dateObs values.
    

Torque-related batch processing arguments
-----------------------------------------

::

   --nodes
   --procs
   


Configuration Parameters
------------------------


