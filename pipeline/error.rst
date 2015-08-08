
.. _errormessages:

======================
Common Pipeline Errors
======================

When a pipeline process fails, it will dump a full stack trace,
showing you what it was doing when the failure occurred.  If you know
what you're looking for, there's a lot of useful information there.
If you don't, it's just a confusing mess.  Below are a few of the most
common blow-ups that you'll run into.  If you've run into an error
that isn't shown here, please let us know so that we can post info
about it here.

If you're having trouble finding the ``stdout``, please see
:ref:`Debugging <debugging>`.


.. _error_setup:

EUPS ``setup`` asks for root password
-------------------------------------

Occassionally, you open a new shell and try to setup the pipeline or
some package, and you see e.g.::

    $ setup -v hscPipe 3.3.3
    You are attempting to run "setup" which requires administrative
    privileges, but more information is needed in order to do so.
    Authenticating as "root"
    Password:

The short answer is that you forgot to ``source`` the EUPS
``setup.sh`` file.  See :ref:`EUPS <back_eups>` for the full details,
but this is what you forgot::

    # If you use a bash shell
    $ source /data1a/ana/products2014/eups/default/bin/setups.sh

    # in a csh shell (or tcsh)
    $ source /data1a/ana/products2014/eups/default/bin/setups.csh

The longer answer is that some Linux systems also have a ``setup``
command which is an administration tool used for system configuration.
When you ``source`` the ``setups.sh`` file (or ``setups.csh``), EUPS
prepends a new directory to your ``PATH`` variable, which hides the
system's ``setup`` command.

.. _error_mapper:

Missing a ``_mapper``
---------------------

In the data repo, there's a file ``_mapper``, which contains the name
of the mapper.  The mapper knows where the data files are located
within the data repo (see :ref:`Data Repo <data_repo>`).  If it's
missing, you'll get an error message like::

    RuntimeError: No mapper provided and no _mapper available

The solution is to create the file yourself.  Here's an example from
the ``master`` system at IPMU::

    $ cat /lustre/Subaru/SSP/_mapper
    lsst.obs.hsc.HscMapper

.. _error_astronetdata:

Missing astrometry_net_data.
----------------------------

By default the pipeline doesn't setup the astrometry_net_data catalog;
or rather, it sets up a dummy version labeled 'none'.  There are two
common ways to hit a problem with this:

#. You forget to run 'setup astrometry_net_data <catalog>'
   
#. You re-setup hscPipe, which then re-setups astrometry_net_data to
   the version 'none'.

The following errors suggest this is might be what happened::

    assert(matches is not None)
    AssertionError

    WARNING: hsc.meas.astrom failed ([Errno 2] No such file or directory: 'none/andConfig.py')

Here's a full stack trace showing this kind of error for an hscProcessCcd.py run::
  
    2014-04-01T01:16:53: processCcd.calibrate: Fit and subtracted background
    2014-04-01T01:16:53: processCcd.calibrate.measurement: Measuring 101 sources
    2014-04-01T01:16:54: processCcd.calibrate.astrometry: Applying distortion \
         correction: HscDistortion derived class
    2014-04-01T01:16:54: processCcd.calibrate.astrometry: Solving astrometry
    2014-04-01T01:16:54: processCcd.calibrate.astrometry WARNING: hsc.meas.astrom \
         failed ([Errno 2] No such file or directory: 'none/andConfig.py')
    2014-04-01T01:16:54: processCcd.calibrate WARNING: Unable to perform astrometry \
         (Unable to solve astrometry for 50, 1_12): attempting to proceed
    2014-04-01T01:16:54: processCcd FATAL: Failed on dataId={'taiObs': '2014-04-01', \
         'pointing': 001, 'visit': 999, 'dateObs': '2014-04-01', 'filter': 'HSC-Y', \
         'field': 'ALIENHOMEWORLD', 'ccd': 50, 'expTime': 200.0}: 
    Traceback (most recent call last):
    File "/data1a/ana/products2014/Linux64/pipe_base/HSC-2.8.1/python/lsst/pipe/base/cmdLineTask.py", line 223, in __call__
       result = task.run(dataRef, **kwargs)
    File "/data1a/ana/products2014/Linux64/hscPipe/2.12.0i_hsc/python/hsc/pipe/tasks/processCcd.py", line 53, in run
       result = ProcessCcdTask.run(self, sensorRef)
    File "/data1a/ana/products2014/Linux64/pipe_base/HSC-2.8.1/python/lsst/pipe/base/timer.py", line 111, in wrapper
       res = func(self, *args, **keyArgs)
    File "/data1a/ana/products2014/Linux64/pipe_tasks/HSC-2.11.1d_hsc/python/lsst/pipe/tasks/processCcd.py", line 82, in run
       result = self.process(sensorRef, postIsrExposure)
    File "/data1a/ana/products2014/Linux64/pipe_base/HSC-2.8.1/python/lsst/pipe/base/timer.py", line 111, in wrapper
       res = func(self, *args, **keyArgs)
    File "/data1a/ana/products2014/Linux64/pipe_tasks/HSC-2.11.1d_hsc/python/lsst/pipe/tasks/processImage.py", line 156, in process
       calib = self.calibrate.run(inputExposure, idFactory=idFactory)
    File "/data1a/ana/products2014/Linux64/pipe_base/HSC-2.8.1/python/lsst/pipe/base/timer.py", line 111, in wrapper
       res = func(self, *args, **keyArgs)
    File "/data1a/ana/products2014/Linux64/pipe_tasks/HSC-2.11.1d_hsc/python/lsst/pipe/tasks/calibrate.py", line 269, in run
       assert(matches is not None)
    AssertionError

.. _error_calib_inputs:
    
Ambiguous calibration inputs
----------------------------

When you created calibration inputs, you specified ``--detrendId
calibVersion=XXX``.  If you made multiple detrends (e.g. biases) with
different ``calibVersions``, the pipeline code will find them and will
not know which one to use.  This is currently not configurable, but
should be soon.  The solution to remove the conflicting detrend.  For
e.g. a flat, it will be located in the data repo in
``CALIB/FLAT/<YYYY-MM-DD>/<FILTER>/<unwanted-calib>``.  Scan the final
line of the error traceback to determine which detrend caused the
trouble.  They're all in ``CALIB/`` in your data repo.

::

     2014-04-01T01:42:26: processCcd FATAL: Failed on dataId={'taiObs': '2014-04-01', \
             'pointing': 100, 'visit': 999, 'dateObs': '2014-04-01', 'filter': 'HSC-Y', \
             'field': 'ALIENHOMEWORLD', 'ccd': 50, 'expTime': 240.0}: \
             Unable to retrieve fringe for {'taiObs': '2014-04-01', 'pointing': 100, \
             'visit': 999, 'dateObs': '2014-04-01', 'filter': 'HSC-Y', \
             'field': 'ALIENHOMEWORLD', 'ccd': 50, 'expTime': 240.0}: \
             No unique lookup for ['calibDate', 'calibVersion'] from {'taiObs': '2014-04-01', \
             'pointing': 100, 'visit': 999, 'dateObs': '2014-04-01', 'filter': 'HSC-Y', \
             'field': 'ALIENHOMEWORLD', 'ccd': 50, 'expTime': 200.0}: 2 matches
     Traceback (most recent call last):
     File "/data1a/ana/products2014/Linux64/pipe_base/HSC-2.8.1/python/lsst/pipe/base/cmdLineTask.py", line 223, in __call__
    result = task.run(dataRef, **kwargs)
    File "/data1a/ana/products2014/Linux64/hscPipe/2.12.0i_hsc/python/hsc/pipe/tasks/processCcd.py", line 53, in run
        result = ProcessCcdTask.run(self, sensorRef)
    File "/data1a/ana/products2014/Linux64/pipe_base/HSC-2.8.1/python/lsst/pipe/base/timer.py", line 111, in wrapper
        res = func(self, *args, **keyArgs)
    File "/data1a/ana/products2014/Linux64/pipe_tasks/HSC-2.11.1d_hsc/python/lsst/pipe/tasks/processCcd.py", line 77, in run
        postIsrExposure = self.isr.run(sensorRef).exposure
    File "/data1a/ana/products2014/Linux64/obs_subaru/HSC-2.17.0b_hsc/python/lsst/obs/subaru/isr.py", line 236, in run
        self.fringe.run(ccdExposure, sensorRef)
    File "/data1a/ana/products2014/Linux64/pipe_base/HSC-2.8.1/python/lsst/pipe/base/timer.py", line 111, in wrapper
        res = func(self, *args, **keyArgs)
    File "/data1a/ana/products2014/Linux64/ip_isr/HSC-2.4.2c_hsc/python/lsst/ip/isr/fringe.py", line 84, in run
        fringes = self.readFringes(dataRef, assembler=assembler)
    File "/data1a/ana/products2014/Linux64/ip_isr/HSC-2.4.2c_hsc/python/lsst/ip/isr/fringe.py", line 113, in readFringes
        raise RuntimeError("Unable to retrieve fringe for %s: %s" % (dataRef.dataId, e))
    RuntimeError: Unable to retrieve fringe for {'taiObs': '2014-04-01', 'pointing': 815, \
        'visit': 999, 'dateObs': '2014-04-01', 'filter': 'HSC-Y', 'field': 'ALIENHOMEWORLD', \
        'ccd': 50, 'expTime': 240.0}: No unique lookup for ['calibDate', 'calibVersion'] from \
        {'taiObs': '2014-04-01', 'pointing': 815, 'visit': 999, 'dateObs': '2014-04-01', \
        'filter': 'HSC-Y', 'field': 'ALIENHOMEWORLD', 'ccd': 50, 'expTime': 200.0}: 2 matches


.. _no_raw_skytile:

no such table: raw_skytile
---------------------------

Chances are you were trying to load some coadd data, but you didn't
provide enough information in your ``dataId`` for the pipeline butler
to do the lookup and get the data.  Here's a short script that will
cause the problem.

.. code-block:: python

    butler = dafPersist.Butler("/path/to/Subaru/HSC/rerun/myrerun/")
    dataId = {'tract': 0, 'patch': '5,5'}
    calexp = butler.get("deepCoadd", dataId)

When run, this will fail as follows::
    
    
    Traceback (most recent call last):
      File "./foo.py", line 13, in <module>
        main()
      File "./foo.py", line 10, in main
        calexp = butler.get("deepCoadd", dataId)
      File "/data1/hsc/products/Linux64/daf_persistence/HSC-3.1.0b_hsc/python/lsst/daf/persistence/butler.py", line 224, in get
        location = self.mapper.map(datasetType, dataId)
      File "/data1/hsc/products/Linux64/obs_subaru/HSC-3.10.1/python/lsst/obs/hsc/hscMapper.py", line 142, in map
        return super(HscMapper, self).map(datasetType, copyId, write=write)
      File "/data1/hsc/products/Linux64/daf_persistence/HSC-3.1.0b_hsc/python/lsst/daf/persistence/mapper.py", line 120, in map
        return func(self.validate(dataId), write)
      File "/data1/hsc/products/Linux64/daf_butlerUtils/HSC-3.3.0g_hsc/python/lsst/daf/butlerUtils/cameraMapper.py", line 285, in mapClosure
        return mapping.map(mapper, dataId, write)
      File "/data1/hsc/products/Linux64/daf_butlerUtils/HSC-3.3.0g_hsc/python/lsst/daf/butlerUtils/mapping.py", line 118, in map
        actualId = self.need(self.keyDict.iterkeys(), dataId)
      File "/data1/hsc/products/Linux64/daf_butlerUtils/HSC-3.3.0g_hsc/python/lsst/daf/butlerUtils/mapping.py", line 201, in need
        lookups = self.lookup(newProps, newId)
      File "/data1/hsc/products/Linux64/daf_butlerUtils/HSC-3.3.0g_hsc/python/lsst/daf/butlerUtils/mapping.py", line 170, in lookup
        where, self.range, values)
      File "/data1/hsc/products/Linux64/daf_butlerUtils/HSC-3.3.0g_hsc/python/lsst/daf/butlerUtils/registries.py", line 170, in executeQuery
        c = self.conn.execute(cmd, values)
    sqlite3.OperationalError: no such table: raw_skytile

    
Here, 'filter' is needed to uniquely identify a coadd dataset, but it
wasn't specified in the ``dataId``.  This fix in this case is (note
the highlighted line):

.. code-block:: python
   :emphasize-lines: 2

    butler = dafPersist.Butler("/path/to/Subaru/HSC/rerun/myrerun/")
    dataId = {'tract': 0, 'patch': '5,5', 'filter': 'HSC-I'}
    calexp = butler.get("deepCoadd", dataId)



.. _column_view:

Cannot get column view to Coord field
-------------------------------------

This type of error occurs when you ask the butler for a
non-native-type as a column view for an array.  The SourceCatalogs can
return column views for ``int`` and ``float``, but non-native types
like 'coord' can't be sliced this way.  This code will fail:

.. code-block:: python

    butler = dafPersist.Butler("/path/to/Subaru/HSC/rerun/myrerun/")
    dataId = {'visit': 1236, 'ccd': 50}
    sources = butler.get("src", dataId)
    coords = sources.get('coord')

    
The failure will be::

    Traceback (most recent call last):
      File "./foo.py", line 15, in <module>
        main()
      File "./foo.py", line 11, in main
        coords = sources.get('coord')
      File "/data1/hsc/products/Linux64/afw/HSC-3.11.0a_hsc/python/lsst/afw/table/tableLib.py", line 8717, in get
        return self[k]
      File "/data1/hsc/products/Linux64/afw/HSC-3.11.0a_hsc/python/lsst/afw/table/tableLib.py", line 8649, in __getitem__
        return self.columns[k]
      File "/data1/hsc/products/Linux64/afw/HSC-3.11.0a_hsc/python/lsst/afw/table/tableLib.py", line 2955, in __getitem__
        return self[self.schema.find(args[0]).key]
      File "/data1/hsc/products/Linux64/afw/HSC-3.11.0a_hsc/python/lsst/afw/table/tableLib.py", line 2958, in __getitem__
        return _tableLib.BaseColumnView___getitem__(self, *args)
    lsst.pex.exceptions.exceptionsLib.LsstCppException: 0: lsst::pex::exceptions::LogicErrorException thrown at python/lsst/afw/table/specializations.i:405 in void lsst_afw_table_BaseColumnView___getitem____SWIG_1(const lsst::afw::table::BaseColumnView*, const lsst::afw::table::Key<lsst::afw::coord::Coord>&)
    0: Message: Cannot get column view to Coord field.


The fix is to loop over sources and call ``get()`` for each coord (note emphasized line):

.. code-block:: python
    :emphasize-lines: 4

    butler = dafPersist.Butler("/path/to/Subaru/HSC/rerun/myrerun/")
    dataId = {'visit': 1236, 'ccd': 50}
    sources = butler.get("src", dataId)
    coords = [src.get("coord") for src in sources]
    
