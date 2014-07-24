
toyShear.py
-----------

Download script :download:`toyShear.py`.

The following demonstrates how to work with moments to convert the
measured adaptive moments, Ixx/Iyy/Ixy to semi-major and semi-minor
axes, and how to convert these to ellipticities of various types.  The
example is meant to represent a toy calculation which might be used in
computing galaxy-galaxy shear.  A central pixel coordinate is chosen,
and the pixel-moments of the sources are rotated from the native x,y
coordinate system to ones defined with respect to the central
position.  The moments are then converted to various ellipticities,
with E1 then representing the tangential (+ve) and radial (-ve)
components.


.. _toyShear:

.. literalinclude:: toyShear.py
   :language: python

