.. role:: red
.. raw:: html
         
   <style> .red {color:red} </style>


.. _detrend:
      
===================================================
Making Detrends (biases, flats, darks, and fringes)
===================================================

Concepts Common to all Detrends
-------------------------------

The commands below show examples for construction of biases, flats,
darks, and fringes.  They were tested on the machine ``master`` at
IPMU.  They should work on any machine, of course, but look carefully
for machine-specific details such as file paths.  You should always be
able to get a full help listing with the command line option '--help',
or simply '-h', e.g.::

   $ reduceFlat.py -h

   
Generating the Calibration Registry
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, the calibration outputs from each command will be written
to the ``CALIB/`` directory (``CALIB/BIAS/``, ``CALIB/DARK``, etc.).  But,
after each command you *must* run ``genCalibRegistry.py`` in order to
make the newly created calibration products available to the system.
On the first run, use ``--create`` option as the registry (a sqlite
database file called ``calibRegistry.sqlite``) will not yet exist.  This
is written explicitly after each command example below::

   $ reduce<Calib>.py [various arguments]
   
   # NOTE: --create is needed only on the first run to create the calibRegistry.sqlite file
   $ genCalibRegistry.py --create --root /data/Subaru/HSC/CALIB --camera HSC --validity 12


The ``--root`` directory should point to ``CALIB/`` in your data
repository, and the ``--validity`` period is the number of days a
given calibration product should be considered stable and useable.  In
the examples here, I've specified 12 days, but that may be too short.
Some users set a much longer validity period, and as of this writing the
length of time the detrends remain stable isn't well known.  Please
use your best judgement.


calibVersions
^^^^^^^^^^^^^

Each type of detrend (bias, flat, fringe) will allow you to specify a
useful label for it with ``calibVersion``.  In the examples below,
I've used 'all' in each case, but labels like 'dome', or 'twilight'
are popular for flats, for example.
   
Biases
------

Biases are constructed using ``reduceBias.py`` located in the hscPipe
package.  There are a number of command line arguments which are
needed.  The filter setting for a bias frame is irrelevant, but you
may see references to a filter in the output from reduceBias.py.  This
simply refers to the filter which was loaded in the exchanger when the
biases were taken, and it does not in any way mean that you can't use
your newly created biases with other filters.

Bias Example 1
^^^^^^^^^^^^^^

::
  
    $ reduceBias.py /data/Subaru/HSC --rerun my_biases --queue small \
        --detrendId calibVersion=all --job bias --nodes 2 --procs 12 \
        --id field=BIAS dateObs=2013-11-04
        
    $ genCalibRegistry.py --create --root /data/Subaru/HSC/CALIB --camera HSC --validity 12
    
The details:

* ``/data/Subaru/HSC`` is the location of the data repository
* ``--rerun my_biases``  is the rerun for the reduced input frames (trimmed, bias subtracted)
* ``--detrendId calibVersion=all``  The final detrend output will be stored with ``calibVersion`` label ``all``.
* ``--id``  allows you to specify which frames to use as inputs.
* PBS Torque options
  * ``--queue small``  The name of the PBS queue
  * ``--job domeI``    The name the job will have when you view it with ``qstat``.
  * ``--nodes 2``      Use 2 compute nodes
  * ``--procs 12``     Run 12 processes on each node.

  
If you try to restart a job which fails, or you try to add data to an
existing rerun, the pipeline will complain as doing this could cause
the rerun to have outputs processed with different processing
parameters.  This is intended to keep you from shooting yourself in
the foot, but it's often necessary during development.  If your not
worried about producing inhomogeneous data (i.e. different outputs
created with different parameters), add ``--clobber-config``.


   
Darks
-----
  
Darks are constructed using ``reduceDark.py`` located in the hscPipe
package. The command line arguments needed are essentially the same as
those required for making biases, so refer back to that section for
details.

Darks Example 1
^^^^^^^^^^^^^^^

::
  
    $ reduceDark.py /data/Subaru/HSC --rerun my_darks --queue small \
        --detrendId calibVersion=all --job darks --nodes 2 --procs 12 \
        --id field=DARK dateObs=2013-11-04

    $ genCalibRegistry.py --root /data/Subaru/HSC/CALIB --camera HSC --validity 12

    
Flats
-----

Flats are constructed using ``reduceFlat.py`` located in the hscPipe
package.  The command line arguments which are needed are essentially
the same as those required for making biases so refer back to that
section for details.  The obvious exception here is that you'll need
to run reduceFlat.py for each filter you observed.  The example shows
only the HSC-I filter.


Flat Example 1
^^^^^^^^^^^^^^

::
  
    $ reduceFlat.py /data/Subaru/HSC --rerun my_dome_i_flats --queue small \
        --detrendId calibVersion=all --job domeI --nodes 2 --procs 12 \
        --id field=DOMEFLAT filter=HSC-I dateObs=2013-11-04 expTime=6.0

    $ reduceFlat.py ... [another filter]
    $ reduceFlat.py ... [yet another filter]
        
    $ genCalibRegistry.py --root /data/Subaru/HSC/CALIB --camera HSC --validity 12

    
Fringes
-------
  
Fringes are constructed using ``reduceFringe.py`` located in the
hscPipe package. The command line arguments needed are essentially the
same as those required for making biases, so refer back to that
section for details.  A few notable distinctions need to be mentioned
here though.

#. The fringes are likely only needed for Y-band.  We haven't found
   any serious fringing in any of the other HSC filters at this time.

#. In all likelihood, you don't need to take special FRINGE
   calibration data.  On-target observations themselves are likely
   sufficient to construct fringe frames.  If you weren't present when
   the data were obtained, it's probably safe to assume the observers
   didn't collect anything special, and you should probably use data
   from targeted observations of some dark field here.  For this
   example, I've used a fictional MYTARGET as a placeholder.  Eligible
   values are those from the OBJECT keywords in your FITS headers, and
   there should be directories in your data repository corresponding
   to each such target from your observing run.

   
Fringe Example 1
^^^^^^^^^^^^^^^^

::
  
    $ reduceFringe.py /data/Subaru/HSC --rerun my_fringe --queue small \
        --detrendId calibVersion=all --job fringe --nodes 2 --procs 12 \
        --id field=MYTARGET dateObs=2013-11-04 filter=HSC-Y
        
    $ genCalibRegistry.py --root /data/Subaru/HSC/CALIB --camera HSC --validity 12

