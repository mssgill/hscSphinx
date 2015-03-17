

==================
Pipeline Structure
==================

The following is an outline of how the pipeline processes each visit.
In the description, there are references to the many Tasks which are
the components of processing.  If you're unfamiliar with Tasks, you
may want to skim through the section explaining the :ref:`core
components <coreComponents>`.


For processing on PBS/Torque, or Slurm cluster, the
``reduceFrames.py`` script uses the ProcessExposureTask.  There are
only two main components to this Task.  Most of the work is done by
``processCcd``, and this Task serves as a way to run the jobs in a
batch on a cluster.  You'll notice that it inherits from a
``BatchPoolTask`` instead of a ``CmdLineTask``::

    hscPipe.ProcessExposureTask(hscPipe.BatchPoolTask)
    
    - processCcd          built with makeSubTask() ... (see SubaruProcessCcdTask below)
    - photometricSolution built with makeSubTask()


The work of the pipeline is performed by ``ProcessCcdTask``.  There's
a Subaru wrapper called ``SubaruProcessCcdTask`` which contains an
additional subtask for quality assurance ``qa``, but this is otherwise
uses ``ProcessCcdTask``.  The heirarchy below shows the structure of
the processing for the pipeline.  The various packages are shown as
namespace prefixes where relevant (e.g. ``meas_alg.`` for
meas_algorithms), and relevant file names are included.  It's
difficult to present a class heirarchy without UML diagrams, but the
following pseudo-code is an attempt to do so::


    hscPipe.SubaruProcessCcdTask(pipe_tasks.ProcessCcdTask)               (hsc/pipe/processExposure.py)
    
    # The SubaruProcessCcdTask directly calls run() on its parent task ProcessCcdTask
    pipe_tasks.ProcessCcdTask(self, dataRef).run()

         # ProcessCcdTask  *is a*  ProcessImageTask
         pipe_tasks.ProcessCcdTask(pipe_tasks.ProcessImageTask)           (pipe/tasks/processCcd.py)

         # subtasks [created with makeSubTask()]
         --> isr:         ip_isr.IsrTask(Task)                            (ip/isr/isr.py)
         --> calibrate:   pipe_tasks.CalibrateTask(Task)                  (pipe/tasks/calibrate.py)

         # Finally, most work is done by ProcessImageTask
         pipe_tasks.ProcessImageTask(self, dataRef).process()
         
              pipe_tasks.ProcessImageTask(pipe_base.CmdLineTask)          (pipe/tasks/processImage.py)

              # subtasks [created with makeSubTask()]
              --> detection:     meas_alg.SourceDetectionTask(Task)       (meas/algorithms/detection.py)
              --> deblend:       meas_alg.SourceDeblendTask(Task)         (meas/algorithms/deblend.py)
              --> measure:       meas_alg.SourceMeasurementTask(Task)     (meas/algorithms/measure.py)
                
    # Final 'qa' processing from SubaruProcessCcdTask
    --> qa:               hsc_pipe.QaTask(Task)                           (hsc/pipe/qa.py)


Notes:

'isr' = 'Instrument Signature Removal' (means bias subtraction, flat fielding, etc.)
        
