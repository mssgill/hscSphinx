
from .config import Config, Field, _joinNamePath, _typeStr
        
class ConfigurableInstance(object):
    """A ConfigurableInstance is the dtype of a ConfigurableField

    A regular Field may refer to a float, int, etc, but a
    ConfigurableField's target is a Task.
    """
    
    def __initValue(self):
        name = _joinNamePath(self._config._name, self._field.name)
        if type(self._field.default)==self.ConfigClass:
            storage = self._field.default._storage
        else:
            storage = {}
        value = self._ConfigClass(__name=name, **storage)
        object.__setattr__(self, "_value", value)

    def __init__(self, config, field):

        # We've overloaded __setattr__, so we set our own attributes
        # with  object.__setattr__(self, "foo", value)
        object.__setattr__(self, "_config", config)
        object.__setattr__(self, "_field", field)
        object.__setattr__(self, "__doc__", config)
        object.__setattr__(self, "_target", field.target)
        object.__setattr__(self, "_ConfigClass",field.ConfigClass)
        object.__setattr__(self, "_value", None)

        self.__initValue()
        
    """ Read-only access """
    target      = property(lambda x: x._target)
    ConfigClass = property(lambda x: x._ConfigClass)
    value       = property(lambda x: x._value)        


    def apply(self, *args, **kw):
        """Instantiate our target class with the given args and kwargs."""
        return self.target(*args, config=self.value, **kw)

    def retarget(self, target, ConfigClass=None):
        """Allow a config to have this name point to a different class.

        This allows a different Task algorithm to be used, and makes the code
        more configurable.
        """
        object.__setattr__(self, "_target", target)
        if ConfigClass != self.ConfigClass:
            object.__setattr__(self, "_ConfigClass",ConfigClass)
            self.__initValue()

    def __getattr__(self, name):
        return getattr(self._value, name)

    def __setattr__(self, name, value):
        self._value.__setattr__(name, value)

    
class ConfigurableField(Field):
    def __init__(self, doc, target, ConfigClass=None, default=None):
        if ConfigClass is None:
            ConfigClass=target.ConfigClass
        if default is None: 
            default=ConfigClass
        self._setup(doc=doc, dtype=ConfigurableInstance, default=default)
        self.target = target
        self.ConfigClass = ConfigClass

    def __getOrMake(self, instance):
        value = instance._storage.get(self.name, None)
        if value is None:
            value = ConfigurableInstance(instance, self)
            instance._storage[self.name]=value
        return value

    def __get__(self, instance, owner=None):
        if instance is None or not isinstance(instance, Config):
            return self
        else:
            return self.__getOrMake(instance)

    def __set__(self, instance, value):
        oldValue = self.__getOrMake(instance)
        if isinstance(value, ConfigurableInstance):
            oldValue.retarget(value.target, value.ConfigClass)
        elif value == oldValue.ConfigClass:
            value = oldValue.ConfigClass()
        oldValue.update(**value._storage)


    def rename(self, instance):
        fullname = _joinNamePath(instance._name, self.name)
        value = self.__getOrMake(instance)
        value._rename(fullname)
        
    def save(self, outfile, instance):        
        fullname = _joinNamePath(instance._name, self.name)
        value = self.__getOrMake(instance)
        target= value.target

        if target != self.target:
            ConfigClass = value.ConfigClass
            for module in set([target.__module__, ConfigClass.__module__]):
                print >> outfile, "import %s" % module
            print >> outfile, "%s.retarget(target=%s, ConfigClass=%s)"%\
                    (fullname, _typeStr(target), _typeStr(ConfigClass))
        value._save(outfile)

