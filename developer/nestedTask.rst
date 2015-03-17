
==========
nestedTask
==========

.. _nestedtask:

The following is Task example which is slightly more complicated than
:ref:`simpleTask.py <simpletask>`.  In this case, there's a main Task
called NestedTask which contains two sub-Tasks: ``Step1`` and
``Step2``.  ``Step2`` is in turn composed of two sub-sub-Tasks
``Step2a`` and ``Step2b``.  The example will work with the simpleTools
code, to use this with the pipeline code, change the imports to::

    import lsst.pex.config        as pexConfig
    import lsst.pipe.base         as pipeBase

To run the ``nestedTask.py`` script (expected output is shown also)::
    
    $ ./nestedTask.py $PWD -j2 --id visit=100..102:2
    Starting the main pipe with:  OrderedDict([('visit', '100')])
    In Step1: OrderedDict([('visit', '100')]) par1 is: 1.0
    In Step2: OrderedDict([('visit', '100')]) par2 is: 2.0
       --> In Sub2a: OrderedDict([('visit', '100')]) par2a is:2.1
       --> In Sub2b: OrderedDict([('visit', '100')]) par2b is:2.2
    Starting the main pipe with:  OrderedDict([('visit', '102')])
    In Step1: OrderedDict([('visit', '102')]) par1 is: 1.0
    In Step2: OrderedDict([('visit', '102')]) par2 is: 2.0
       --> In Sub2a: OrderedDict([('visit', '102')]) par2a is:2.1
       --> In Sub2b: OrderedDict([('visit', '102')]) par2b is:2.2

.. literalinclude:: simpleTools/nestedTask.py

