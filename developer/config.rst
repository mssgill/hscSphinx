

======
Config
======

.. _minipipe_config:

The config code is located in the pex_config module.  Here we describe
the main components, which are located in two files:

In pex_config: ``python/lsst/pex/config/config.py``, and
``python/lsst/pex/config/configurableField.py``.

Field
-----

A specific config parameter is defined in a Field.  This will contain
the parameter's type, a short documentation string, and a default
value.
    
ConfigMeta
----------

This is a *meta class* which is used to create Config classes.  This
is not a simple concept and requires some understanding of how Python
classes are themselves treated as objects.  If this topic is
unfamiliar, a helpful introduction to metaclasses can be found `here
<http://eli.thegreenplace.net/2011/08/14/python-metaclasses-by-example>`_.
    
Config
------

This is base class for all Config classes.


ConfigurableInstance, ConfigurableField
---------------------------------------

When a Config class refers to a parameter which is a Task rather than
e.g. float, int, etc.; it will be defined as a ``ConfigurableField``,
and will have type ``ConfigurableInstance``.


config.py
---------

The following includes only the essential components of ``config.py``.
The overall functionality is preserved, but this code is not intended
to be as robust or rigorous as that used by the pipeline.  It is
intended to demonstrate the design without extra complexity required
by the pipeline.

.. literalinclude:: simpleTools/lsst_pex_config/config.py
   :language: python


configurableField.py
--------------------

.. literalinclude:: simpleTools/lsst_pex_config/configurableField.py
   :language: python

