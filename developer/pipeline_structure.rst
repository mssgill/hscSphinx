

=====================
Pipeline Structure
=====================

* how does a task work?




* processExposureTask hierarchy::

    hscPipe.ProcessExposureTask(hscPipe.PbsCmdLineTask)
    
    --> processCcd          makeSubTask ... (a SubaruProcessCcdTask)
    --> photometricSolution makeSubTask
    
    hscPipe.SubaruProcessCcd(pipe_tasks.ProcessCcdTask)
    
        --> qa     makeSubTask('qa')
        pipe_tasks.ProcessCcd().run()
        
        pipe_tasks.ProcessCcdTask(ProcessImageTask)
            --> isr  [makeSubTask('isr')]
            
            pipe_tasks.ProcessImageTask(CmdLineTask)
            
                --> calibrate   makeSubTask('calibrate')
                --> detection   makeSubTask('detection')
                    SourceDetectionTask(Task) (in meas_alg)
                --> deblend     makeSubTask('deblend')
                    SourceDeblendTask(Task) (in meas_alg)
                --> measure     makeSubTask('measure')
                    SourceMeasurementTask(Task) (in meas_alg)
                     
                --> doWriteCalibrate (why isn't this a Task?)
                
                pipe_base.CmdLineTask(Task)



                
