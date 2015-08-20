#!/usr/bin/env python

import sys

import lsst_pex_config     as pexConfig
import lsst_pipe_base      as pipeBase

#########################################################
# Step 1
#########################################################
class Step1Config(pexConfig.Config):
    """Configration for Step1"""
    par1 = pexConfig.Field("parameter 1", float, 1.0)
class Step1Task(pipeBase.Task):
    """Task which runs Step1"""
    ConfigClass = Step1Config
    def run(self, dataRef, **kwargs):
        print "In Step1:", dataRef, "par1 is:", self.config.par1

        
#########################################################
# Step 2
#########################################################
class Sub2aConfig(pexConfig.Config):
    """Configration for Step2a"""
    par2a = pexConfig.Field("parameter 2a", float, 2.1)
class Sub2aTask(pipeBase.Task):
    """Task which runs Step2a"""
    ConfigClass = Sub2aConfig
    def run(self, dataRef, **kwargs):
        result = pipeBase.Struct(result= "In Sub2a: "+str(dataRef)+" par2a is:"+str(self.config.par2a))
        return result
        
class Sub2bConfig(pexConfig.Config):
    """Configration for Step2b"""
    par2b = pexConfig.Field("parameter 2b", float, 2.2)
class Sub2bTask(pipeBase.Task):
    """Task which runs Step2b"""
    ConfigClass = Sub2bConfig
    def run(self, dataRef, **kwargs):
        result = pipeBase.Struct(result= "In Sub2b: "+str(dataRef)+" par2b is:"+str(self.config.par2b))
        return result

class Step2Config(pexConfig.Config):
    """Configration for Step2"""
    par2   = pexConfig.Field("parameter 2", float, 2.0)
    sub2a  = pexConfig.ConfigurableField("Sub2a task", target=Sub2aTask)
    sub2b  = pexConfig.ConfigurableField("Sub2b task", target=Sub2bTask)
class Step2Task(pipeBase.Task):
    """Task which runs Step2"""
    ConfigClass = Step2Config
    def __init__(self, *args, **kwargs):
        super(Step2Task, self).__init__(*args, **kwargs)
        self.makeSubtask("sub2a")
        self.makeSubtask("sub2b")
    def run(self, dataRef, **kwargs):
        print "In Step2:", dataRef, "par2 is:", self.config.par2
        sub2a = self.sub2a.run(dataRef, **kwargs)
        print "   -->", sub2a.result
        sub2b = self.sub2b.run(dataRef, **kwargs)
        print "   -->", sub2b.result


#########################################################
# Main Task
#########################################################
class NestedConfig(pexConfig.Config):
    """Configration for NestedTask"""
    doStep1  = pexConfig.Field("Run Step 1 processing", bool, True)
    step1    = pexConfig.ConfigurableField("Step1 task", target=Step1Task)
    doStep2  = pexConfig.Field("Run Step2 processing", bool, True)
    step2    = pexConfig.ConfigurableField("Step2 task", target=Step2Task)

class NestedTask(pipeBase.CmdLineTask):
    """NestedTask which runs Step1 and Step2 Tasks"""
    _DefaultName = "mini"
    ConfigClass  = NestedConfig
    
    def __init__(self, *args, **kwargs):
        super(NestedTask, self).__init__(*args, **kwargs)
        self.makeSubtask("step1")
        self.makeSubtask("step2")
        
    def run(self, dataRef, **kwargs):
        print "Starting the main pipe with: ", dataRef
        if self.config.doStep1:
            self.step1.run(dataRef, **kwargs)
        if self.config.doStep2:
            self.step2.run(dataRef, **kwargs)


#########################################################
# Main entry point (typically in a separate file)
#########################################################
if __name__ == '__main__':
    NestedTask.parseAndRun(sys.argv[1:])
