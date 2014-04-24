
=============
Quick Summary
=============

Assuming you've read the other sections, these commands will all make perfect since.

#. Setup::

     $ . /data1a/ana/products2014/eups/defaults/bin/setup.sh
     $ setup -v hscPipe -t HSC
     $ setup -v astrometry_net_data ps1_pv1.2a
    
#. Ingest the rawdata::

     $ mkdir /path/to/HSC
     $ cd /path/to/rawdata/
     $ hscIngestImages.py /path/to/HSC/ --create --mode=link HSCA*.fits

#. Run the single frame processing::

     $ reduceFrames.py /path/to/HSC/ --rerun

    
