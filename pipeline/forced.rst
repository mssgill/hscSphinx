
.. _forced:

=================
Forced Photometry
=================

Forced photometry is a process in which the coordinates from
detections made in one image are used to perform measurements in
another image.  Typically the detection image is a specific filter,
e.g. HSC-I, and the forced image was taken with a different filter.
However, another common type of 'forced' measurement involves using
coordinates from detections in deeper coadds to force-measure sources
in the input images.

Once you've completed the earlier stages in the pipeline, you can use
your coadd measurements to force measurements in your single-frame
data::

    $ forcedPhotCcd.py /data/Subaru/HSC --rerun=myrerun --id visit=1234 ccd=0..103 tract=0


