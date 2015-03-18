
.. _detectfewer:

detectFewer.py
--------------

This code creates Config and Task classes which inherit from
``meas_algorithms.SourceDetectionConfig`` and
``meas_algorithms.SourceDetectionTask``.  The purpose here is to
insert this task in the pipeline so that it runs instead of the normal
``SourceDetectionTask``.  The details aren't all that important, and
the main point is to demonstrate how to replace a pipeline task.

The example code is very simple, defining an ``nObjects`` config
parameter to specify the number of detected footprints to keep
(default set to 400).  This was done to allow the code to run faster
for debugging.

By inheriting from the original SourceDetectionTask/Config, we
automatically get the capabilities of that Task.  The pipeline's
SourceDetectionTask uses a method ``makeSourceCatalog()`` which
performs detection and makes the sources.  So all we need to do is
overload that method with one that keeps ``nObject`` detections.  We
then use a config retarget to tell the pipeline to use our Task
instead of the default.

The config retarget is defined in a file just as any config overrides
would be (notice that detection is called twice in the pipeline, so we
retarget for each case)::

    $ cat my-fast-overrides.config
    import detectFewer
    root.calibrate.detection.retarget(detectFewer.FewerSourceDetectionTask)
    root.detection.retarget(detectFewer.FewerSourceDetectionTask)

``hscProcessCcd.py`` can then be run with this override file::

    $ hscProcessCcd.py /path/to/data/ --rerun=myrerun --id visit=100 ccd=50 -C my-fast-overrides.config
    
The ``detectFewer.py`` code is the following::

    import random
    import lsst.pex.config as pexConfig
    import lsst.pipe.base as pipeBase
    import lsst.afw.table as afwTable
    import lsst.meas.algorithms as measAlg

    class FewerSourceDetectionConfig(measAlg.SourceDetectionConfig):
        nObjects = pexConfig.Field(doc="Number of sources to select", dtype=int, optional=False, default=400)

    class FewerSourceDetectionTask(measAlg.SourceDetectionTask):
        """This task serves only to cull the source list and make measurement faster"""

        ConfigClass = FewerSourceDetectionConfig

        def makeSourceCatalog(self, table, exposure, doSmooth=True, sigma=None, clearMask=True):
            if self.negativeFlagKey is not None and self.negativeFlagKey not in table.getSchema():
                raise ValueError("Table has incorrect Schema")
            
            # detect the footprints as usual
            fpSets = self.detectFootprints(exposure=exposure, doSmooth=doSmooth, sigma=sigma,
                                           clearMask=clearMask)

            # shuffle the footprints to ensure they're random across the frame
            n = self.config.nObjects
            fpPos = fpSets.positive.getFootprints()
            random.shuffle(fpPos)

            # delete the excess footprints, and the negative footprints
            del fpPos[n:]
            fpSets.numPos = n
            if fpSets.negative:
                del fpSets.negative.getFootprints()[0:]
                fpSets.negative = None

            # make sources
            sources = afwTable.SourceCatalog(table)
            table.preallocate(fpSets.numPos)
            if fpSets.positive:
                fpSets.positive.makeSources(sources)

            return pipeBase.Struct(sources=sources, fpSets=fpSets)
