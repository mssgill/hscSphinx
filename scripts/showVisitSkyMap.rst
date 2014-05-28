

showVisitSkyMap.py
------------------

Download script :download:`showVisitSkyMap.py`.

The following demonstrates how to load and display a SkyMap and the
CCDs in a set of visits.  Comments are brief (apologies), but the
script is quite short.

.. warning::

    The camera-related code has already been rewritten in the LSST
    fork of the pipeline, and the new implementation will eventually
    be imported into the HSC fork.  We will naturally update the
    documentation accordingly when that happens, but please be aware
    that if you develop new code based on what you see here, it too
    will have to be updated.

.. _showvisitskymap:

.. literalinclude:: showVisitSkyMap.py
   :language: python


To run::

    $ python skymap.py /data2b/work/bick/HSC/rerun/cosmos 0 902^904 -p

Output
^^^^^^

.. image:: ../images/showVisitSkyMap.png

