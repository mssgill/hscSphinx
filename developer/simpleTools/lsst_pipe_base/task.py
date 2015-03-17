
# original file in pipe_base: python/lsst/pipe/base/task.py

class Task(object):
    """Base class for encapsulating a single component of data processing."""
    
    def __init__(self, config=None, name=None, parentTask=None):
        if parentTask is not None:
            self._name = name
            self._fullName = parentTask._computeFullName(name)
            if config == None:
                config = getattr(parentTask.config, anme)
            self._taskDict = parentTask._taskDict
        else:
            if name is None:
                name = self._DefaultName
            self._name = name
            self._fullName = self._name
            if config is None:
                config = self.ConfigClass()
            self._taskDict = dict()
        self.config = config
        self._taskDict[self._fullName] = self

    def makeSubtask(self, name, **keyArgs):
        """Construct a specified subtask.

        Sub-tasks will be ConfigurableField's in the Config class.  The
        target of a ConfigurableField will itself by another Task.
        """
        configurableField = getattr(self.config, name, None)
        subtask = configurableField.apply(name=name, parentTask=self, **keyArgs)
        setattr(self, name, subtask)

    def run(self, dataRef, **kwargs):
        """A virtual method to be defined by derived classes"""
        pass

    def _computeFullName(self, name):
        return "%s.%s" % (self._fullName, name)
        

