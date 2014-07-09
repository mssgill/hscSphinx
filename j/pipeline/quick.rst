
=============
Quick Summary
=============

Assuming you've read the other sections, these commands will all make
perfect sense. This should be a complete listing of the commands you
need in order to process a set of PI observations from beginning to
end.  This hypothetical data includes calibration exposures for BIAS,
DARK, and DOMEFLAT, and assumes the target field is called "COSMOS",
and it has been observed in HSC-I band in visits 100 to 200 with
increment 2 (i.e. 100..200:2).  **You'll have to adjust the target
field name and visit numbers to match your data.**.


#. Setup (:ref:`full details <back_eups>`)::

     $ . /data1a/ana/products2014/eups/defaults/bin/setup.sh
     $ setup -v hscPipe -t HSC
     $ setup -v astrometry_net_data ps1_pv1.2a
    
#. Ingest the rawdata (:ref:`full details <ingest>`)::

     $ mkdir /data/Subaru/HSC
     $ cd /path/to/rawdata/
     $ hscIngestImages.py /data/Subaru/HSC/ --create --mode=link HSCA*.fits

#. Construct calibration frames (:ref:`full details <detrend>`)::

     $ reduceBias.py /data/Subaru/HSC/ --rerun all_bias --queue small --detrendId calibVersion=all --job bias --nodes=3 --procs=12 --id field=BIAS
     $ genCalibRegistry.py --create --root /data/Subaru/HSC/CALIB --camera HSC --validity 12

     $ reduceDark.py /data/Subaru/HSC/ --rerun all_dark --queue small --detrendId calibVersion=all --job dark --nodes=3 --procs=12 --id field=DARK
     $ genCalibRegistry.py --root /data/Subaru/HSC/CALIB --camera HSC --validity 12
     
     $ reduceFlat.py /data/Subaru/HSC --rerun dome_flats --queue small --detrendId calibVersion=domeflat --job dflat --nodes=3 --procs=12 --id field=DOMEFLAT
     $ genCalibRegistry.py --root /data/Subaru/HSC/CALIB --camera HSC --validity 12

     # use data from the target itself to construct fringes
     $ reduceFringe.py /data/Subaru/HSC/ --rerun all_fringe --queue small --detrendId calibVersion=all --job fringe --nodes=3 --procs=12 --id field=COSMOS
     $ genCalibRegistry.py --root /data/Subaru/HSC/CALIB --camera HSC --validity 12

#. Determine which visits we have to process for e.g. HSC-I data (:ref:`full details <registryinfo>`)::

     $ export SUPRIME_DATA_DIR=/data/Subaru/HSC
     $ registryInfo.py --field COSMOS --filter HSC-I
     <list of visits>
     
#. (optional) Test running one CCD from the ``registryInfo.py list`` (:ref:`full details <hscprocessccd>`)::

     $ hscProcessCcd.py /data/Subaru/HSC/ --rerun cosmos --id visit=100 ccd=50
     
#. Run the single frame processing (:ref:`full details <reduceframes>`)::

     $ reduceFrames.py /data/Subaru/HSC/ --rerun cosmos --id field=COSMOS visit=100..200:2


..     
   #. (optional) Run single-frame QA on some select visits (e.g. visit number 100)::

   $ cat .pqa/dbauth.py
   $ cat .hsc/dbauth.py
   $ mkdir -p /home/you/public_html/qa
   $ export WWW_ROOT=/home/you/public_html/qa
   $ export WWW_RERUN=cosmos
   $ export TESTBED_PATH=/data/Subaru/HSC/rerun
   $ newQa.py -p hsc cosmos
   $ pipeQa.py -d butler -C hsc -v 100 cosmos

   
#. Make a SkyMap (assuming you want a partial SkyMap) (:ref:`full details <skymap>`)::

    $ makeDiscreteSkyMap.py /data/Subaru/HSC/ --rerun=cosmos --id visit=100..200:2 ccd=0..103

#. Run mosaic (ubercal) (:ref:`full details <mosaic>`)::

    $ mosaic.py /data/Subaru/HSC --rerun cosmos --id tract=0 visit=100..200:2 ccd=0..103

#. Coadd Processing (:ref:`full details <stack>`)::

    $ stack.py /data/Subaru/HSC/ --rerun=cosmos --id tract=0 filter=HSC-I \
          --selectId visit=100..200:2 --queue small --nodes 4 --procs 6 --job stack
