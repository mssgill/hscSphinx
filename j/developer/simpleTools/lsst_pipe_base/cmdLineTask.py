
# original file: pipe_base - python/lsst/pipe/base/cmdLineTask.py

import multiprocessing
from .task   import Task
import struct
import argumentParser   as argParse

class TaskRunner(object):
    """A class to handle running a CmdLineTask object."""
    
    def __init__(self, TaskClass, parsedCmd):
        self.TaskClass    = TaskClass
        self.config       = parsedCmd.config
        self.numProcesses = parsedCmd.processes
        
    def run(self, parsedCmd):
        """Instantiate and call run() on the Task we're responsible for.
        
        Use multiprocessing to run with multiple threads, if requested.
        """
        targets    = self.getTargetList(parsedCmd)
        if self.numProcesses > 1:
            pool       = multiprocessing.Pool(processes=self.numProcesses, maxtasksperchild=1)
            mapFunc    = pool.map
        else:
            pool       = None
            mapFunc    = map
            
        # we have overloaded __call__, so we pass self to map() as a callable function.
        resultList = mapFunc(self, targets)
        if pool:
            pool.close()
            pool.join()
        return resultList
        
    @staticmethod
    def getTargetList(parsedCmd, **kwargs):
        """Get the dataRefs requested on the command line.

        We return a list, with each entry to be passed to us as arguments
        for our __call__() method.
        getTargetList() can therefore be overloaded to change
        how a task is instantiated and run.
        """
        return [(ref, kwargs) for ref in parsedCmd.id.refList]

    def makeTask(self):
        """Instantiate the task we are responsible for."""
        return self.TaskClass(config=self.config)
        
    def __call__(self, args):
        """Instantiate our tast, and call run()"""
        dataRef, kwargs = args
        task   = self.makeTask()
        result = task.run(dataRef, **kwargs)
        return struct.Struct(dataRef=dataRef, result=result)


class CmdLineTask(Task):
    """A derived Task which can be used to create an executable Python script"""
    
    _DefaultName = "default"
    RunnerClass  = TaskRunner
    
    @classmethod
    def parseAndRun(cls, args):
        """Parse command line arguments, make a TaskRunner, and run this task."""
        argumentParser = cls._makeArgumentParser()
        config         = cls.ConfigClass()
        parsedCmd      = argumentParser.parse_args(config=config, args=args)
        taskRunner     = cls.RunnerClass(TaskClass=cls, parsedCmd=parsedCmd)
        resultList     = taskRunner.run(parsedCmd)
        return struct.Struct(
            argumentParser = argumentParser,
            parsedCmd      = parsedCmd,
            taskRunner     = taskRunner,
            resultList     = resultList,
        )
        
    @classmethod
    def _makeArgumentParser(cls):
        parser = argParse.ArgumentParser(name=cls._DefaultName)
        parser.add_id_argument(name="--id", datasetType='raw', help="id parameters")
        return parser


