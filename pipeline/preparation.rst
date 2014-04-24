

============
Preparation
============


EUPS
----

* what is eups

* source setups.sh

  * eups -h
  
* setup -v hscPipe

  * versions
    
  * tags -t HSC

  
* eups list

  * eups list product*

  * eups list -s product

    
Setting up for the run
^^^^^^^^^^^^^^^^^^^^^^

* get the correct eups setups

  * Setup the pipeline::

    $ setup -v hscPipe -t HSC

  * Setup the calibration catalog.  CHOOSE ONLY ONE!  A `setup` command will override it's predecessor!::
    
    # perhaps use PS1
    $ setup -v astrometry_net_data ps1_pv1.2a
    
    # *OR* perhaps use SDSS DR8
    $ setup -v astrometry_net_data sdss-dr8

