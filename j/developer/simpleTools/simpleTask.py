#!/usr/bin/env python
import sys
import lsst_pex_config as pexConfig
import lsst_pipe_base  as pipeBase

class SimpleConfig(pexConfig.Config):
    doThis  = pexConfig.Field("Run this processing", bool, True)
    x       = pexConfig.Field("A decimal number", float, 3.14159)
    n       = pexConfig.Field("Maximum number of iterations", int, 3)
    
class SimpleTask(pipeBase.CmdLineTask):
    _DefaultName = "simple"
    ConfigClass  = SimpleConfig
    
    def run(self, dataRef, **kwargs):
        print "Starting the main pipe with: ", dataRef

        if self.config.doThis:
            for i in range(self.config.n):
                print i, i*self.config.x
                
        print "Finished: ", dataRef
        
if __name__ == '__main__':
    SimpleTask.parseAndRun(sys.argv[1:])
