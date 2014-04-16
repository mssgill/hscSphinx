

===================================================
Making Detrends (biases, flats, darks, and fringes)
===================================================

The commands below show examples for construction of biases, flats, darks, and fringes.  They were tested on the machine ``master`` at IPMU.  They should work on any machine, of course, but look carefully for machine-specific details such as file paths.  You should always be able to get a full help listing with the command line option '--help', or simply '-h', e.g.::

   $ reduceFlats.py -h


Biases
------

Biases are constructed using ``reduceBias.py`` located in the hscPipe package.  There are a number of command line arguments which are needed.

Bias Example 1
^^^^^^^^^^^^^^

::
  
    $ reduceBias.py /data/Subaru/HSC --rerun my_biases --queue small \
        --detrendId calibVersion=all --job bias --nodes 2 --procs 12 \
        --time 2000000 --id field=BIAS dateObs=2013-11-04 expTime=6.0

The details:

* ``/data/Subaru/HSC`` is the location of the data repository
* ``--rerun my_dome_i_flats``  is the rerun for the reduced input frames (trimmed, bias subtracted)
* ``--detrendId calibVersion=all``  The final output flats will be stored with ``calibVersion`` label ``all``.
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
the foot, but it's often necessary during development.  If your foot
has it coming, add ``--clobber-config``.


   
Darks
-----
  
Darks are constructed using ``reduceDarks.py`` located in the hscPipe package. The command line arguments needed are essentially the same as those required for making biases, so refer back to that section for details.

Darks Example 1
^^^^^^^^^^^^^^^

::
  
    $ reduceDarks.py /data/Subaru/HSC --rerun my_darks --queue small \
        --detrendId calibVersion=all --job darks --nodes 2 --procs 12 \
        --time 2000000 --id field=DARKS dateObs=2013-11-04 expTime=6.0

   
Fringes
-------
  
Fringes are constructed using ``reduceFringe.py`` located in the hscPipe package. The command line arguments needed are essentially the same as those required for making biases, so refer back to that section for details.

Fringe Example 1
^^^^^^^^^^^^^^^^

::
  
    $ reduceFringe.py /data/Subaru/HSC --rerun my_fringe --queue small \
        --detrendId calibVersion=all --job fringe --nodes 2 --procs 12 \
        --time 2000000 --id field=FRINGE dateObs=2013-11-04 expTime=6.0
        

Flats
-----

Flats are constructed using ``reduceFlat.py`` located in the hscPipe package.  The command line arguments which are needed are essentially the same as those required for making biases so refer back to that section for details.

Flat Example 1
^^^^^^^^^^^^^^

::
  
    $ reduceFlat.py /data/Subaru/HSC --rerun my_dome_i_flats --queue small \
        --detrendId calibVersion=all --job domeI --nodes 2 --procs 12 \
        --time 2000000 --id field=DOMEFLAT filter=HSC-I dateObs=2013-11-04 expTime=6.0


