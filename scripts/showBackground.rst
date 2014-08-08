
.. _showbackground:


showBackground.py
-----------------

Download script :download:`showBackground.py`.

The following demonstrates how to load a calexp exposure, and is very
similar to the :ref:`ccdplot.py <ccdplot>` example.  However, since the
backgrounds are already subtracted in the calexp images, and some users
wish to perform their own background subtraction, this example
also demonstrates loading the background image and adding it to the
calexp to recover the pre-background-subtracted image.


.. literalinclude:: showBackground.py
   :language: python

