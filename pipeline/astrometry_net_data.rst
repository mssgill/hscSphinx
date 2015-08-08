
.. _astrometry_net_data:

====================
Astrometry_net_data
====================

.. note:: credit where credit is due.  This section was lifted word-for-word from: http://hsca.ipmu.jp:8080/question/37/question-astrometry-cat-in-hsc-pipeline/.

The astrometry_net_data product distributed with the pipeline is a
placeholder, and not a real astrometry catalogue. You need to obtain,
declare and setup a proper astrometry_net_data.

How to obtain astrometry_net_data
---------------------------------

If you have an account on another machine that has some
astrometry_net_data catalogues (e.g., the IPMU clusters), you can copy
over the directories listed when you do::

    $ eups list -d astrometry_net_data
    
If you can't do that, you can get the 2mass catalogue from
astrometry.net. It will need an additional file called andConfig.py
that looks like this::

    root.defaultMagColumn = "j_mag" # Default column name to use for magnitudes
    root.magColumnMap = { 'J': 'j_mag' } # Mapping from filter to magnitude column name
    root.magErrorColumnMap = {} # Mapping from filter to magnitude error column name
    root.indexFiles = ['index-130202000-00.fits',
                       'index-130202000-01.fits',
                       # Etc, listing all the index files
                       ]
                       
There is also an SDSS DR8 catalog that you can download from here.

Declaring
----------

For each astrometry_net_data directory you've downloaded, you need to::

    $ eups declare astrometry_net_data <version> -r /path/to/astrometry_net_data/<version> -m none
    
When I have multiple directories, you find this convenient::

    $ cd /path/to/astrometry_net_data
    $ for d in *; do eups declare astrometry_net_data $d -r $d -m none; done
    
Setup
-----

Once the catalogue you want has been declared to eups, you should set
it up so you can use it::

    $ setup -j astrometry_net_data <version>
    
    # e.g.;
    $ setup -j astrometry_net_data sdss-dr8
    
The -j flag means only setup this product: it doesn't mess with any
dependencies. This is important because without it, it will try to
unsetup the dependencies (e.g., gcc and python), and leave you in a
bad state.

You will need to setup the astrometry_net_data in each new
environment, e.g., whenever you setup -t HSC hscPipe.
