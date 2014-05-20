
print_coord.py
--------------

Download script :download:`print_coord.py`.

The following demonstrates how to work with Coord objects loaded
through the butler.  Coords are converted between the various types
(ICRS, FK5, Galactic, Ecliptic), and the Angle objects used for each
dimension of the coordinate (i.e. RA and Dec are each Angles) are
printed in various standard forms.


.. _print_coord:

.. literalinclude:: print_coord.py
   :language: python

