
============================
Machine Specific Information
============================

This section contains information needed to work on specific machines.  

master
------

**EUPS setups** file to source (only bash shell shown)::

    $ source /data1a/ana/products2014/eups/default/bin/setups.sh
    
**Location of data repository**.  This is handled with a special eups
  command which sets the ``$SUPRIME_DATA_DIR`` environment variable::

    $ setup -v suprime_data

    $ echo $SUPRIME_DATA_DIR 
    /lustre/Subaru/SSP
    
