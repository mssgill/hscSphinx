
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

#. Construct calibration frames::

     $ reduceBias.py /path/to/HSC/ --rerun all_bias --queue small --detrendId calibVersion=all --job bias --nodes=3 --procs=12 --id field=BIAS
     $ genCalibRegistry.py --create --root /data/Subaru/HSC/CALIB --camera HSC --validity 12

     $ reduceDark.py /path/to/HSC/ --rerun all_dark --queue small --detrendId calibVersion=all --job dark --nodes=3 --procs=12 --id field=DARK
     $ genCalibRegistry.py --root /data/Subaru/HSC/CALIB --camera HSC --validity 12
     
     $ reduceFlat.py /path/to/HSC --rerun dome_flats --queue small --detrendId calibVersion=domeflat --job dflat --nodes=3 --procs=12 --id field=DOMEFLAT
     $ genCalibRegistry.py --root /data/Subaru/HSC/CALIB --camera HSC --validity 12
     
     $ reduceFringe.py /path/to/HSC/ --rerun all_fringe --queue small --detrendId calibVersion=all --job fringe --nodes=3 --procs=12 --id field=MYTARGET
     $ genCalibRegistry.py --root /data/Subaru/HSC/CALIB --camera HSC --validity 12
     
#. (optional) Test running one CCD::

     $ hscProcessCcd.py /path/to/HSC/ --rerun my_data
     
#. Run the single frame processing::

     $ reduceFrames.py /path/to/HSC/ --rerun my_data


..     
   #. (optional) Run single-frame QA on some select visits (e.g. visit number 1000)::

   $ mkdir -p /home/you/public_html/qa
   $ export WWW_ROOT=/home/you/public_html/qa
   $ export WWW_RERUN=my_qa
   $ export TESTBED_PATH=/path/to/HSC/rerun
   $ newQa.py -p hsc my_qa
   $ pipeQa.py -d butler -C hsc -v 1000 my_data

   
#. Make a SkyMap (assuming you want a partial SkyMap)::

    $ makeDiscreteSkyMap.py /path/to/HSC/ --rerun=myrerun --id visit=1000..1020:2

    
#. Coadd Processing::

    $ stack.py /path/to/HSC/ --rerun=myrerun --id tract=0 \
          --selectId visit=1000..1020:2 --queue small --nodes 4 --procs 6 --job stack
