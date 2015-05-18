

==================
Writing Real Tasks
==================

The following descripts how to write ``CmdLineTasks`` in various
levels of difficulty.  These code examples use the real pipeline and
are intended to demonstrate the sorts of things you might actually
want to do.

Reasons you might want to consider writing a Task include things like:

* You want to take advantage of the built-in handling of DataIds and parallel processing
* You want to run the pipeline in a way that's significantly different from the default

The general form of a Task inheriting from CmdLineTask should be as
shown below.  Note that there are three ``_get<>Name()`` methods that
you need to overload to return None!  These are normally used
internally by the pipeline to keep track of configuration parameters
and package versions.  They're needed for the task to run, but they
should return ``None``, and you can otherwise ignore them::

    #!/usr/bin/env python
    import lsst.pipe.base as pipeBase
    import lsst.pex.config as pexConfig
    
    class MyTask(pipeBase.CmdLineTask):
        _DefaultName = 'mytask'
        ConfigClass = pexConfig.Config()
        
        def run(self, dataRef):

            ################################
            # do something with this dataRef
            ################################
            
            return
            
        # Overload these if your task inherits from CmdLineTask
        def _getConfigName(self):
            return None
        def _getEupsVersionsName(self):
            return None
        def _getMetadataName(self):
            return None
            
    if __name__ == '__main__':
        MyTask.parseAndRun()

        
The examples below use this basic structure to do a some fairly simple
things with pipeline data.


.. toctree::
   :hidden:

   findTract
   detectFewer
   
:ref:`findTract.py <findtract>`

    This is a short example which creates a CmdLineTask to look-up the
    tract for a given visit,CCD.

:ref:`detectFewer.py <detectFewer>`

    This demonstrates how to write a Task to override a pipeline Task
    and change the behaviour of part of the pipe.  The example
    replaces the pipeline's SourceDetectionTask with one
    that reduces the number of detections, allowing the pipeline
    to run faster when debugging.

    
    
.. findTract
.. runAFew
.. runPostISRCCD
