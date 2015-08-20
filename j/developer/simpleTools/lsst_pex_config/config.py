#!/usr/bin/env python
import sys, io
import copy

def _joinNamePath(prefix=None, name=None):
    """Helper function to concatenate prefix and name with '.'"""
    tmp = prefix
    if prefix and name:
        tmp += "." + name
    return tmp


def _typeStr(x):
    """Helper function to get the type as a string"""
    if hasattr(x, '__module__') and hasattr(x, '__name__'):
        xtype = x
    else:
        xtype = type(x)
    if xtype.__module__ == '__builtin__':
        return xtype.__name__
    else:
        return "%s.%s"%(xtype.__module__, xtype.__name__)


class Field(object):
    """
    Each attribute of a Config class shall be a Field object.
    It contains the dtype, default value, set value, and some documentation
    """
    
    def __init__(self, doc, dtype, default=None):
        self._setup(doc=doc, dtype=dtype, default=default)
        
    def _setup(self, doc, dtype, default):
        self.dtype   = dtype
        self.doc     = doc
        self.__doc__ = doc
        self.default = default

    def _validateValue(self, value):
        if value is None:
            return
        if not isinstance(value, self.dtype):
            msg = "Value %s is of incorrect type %s. Expected type %s"%\
                    (value, _typeStr(value), _typeStr(self.dtype))
            raise TypeError(msg)
        
    def save(self, outfile, instance):
        """Print ourself to outfile."""
        value = self.__get__(instance)
        fullname = _joinNamePath(instance._name, self.name)
        doc = "'''" + self.doc + " '''"
        print >> outfile, "%s\n%s=%r\n"%(doc, fullname, value)
            
    def rename(self, instance):
        pass
        
    def __get__(self, instance, label=None):
        if instance is None or not isinstance(instance, Config):
            return self
        else:
            return instance._storage[self.name]

    def __set__(self, instance, value):
        if value is not None:
            if self.dtype==float and type(value)==int:
                value = float(value)
            self._validateValue(value)
        instance._storage[self.name] = value


            
class ConfigMeta(type):
    """A metaclass for a config

    A metaclass is used to define a class
    (note we inherit from 'type', not 'object')
    If this is a new concept, good descriptions are found at:
    http://eli.thegreenplace.net/2011/08/14/python-metaclasses-by-example
    
    This class will be called to *create* a config class
    by recursing the class attributes which are of type Config until
    we find attributes of type Field.  These are set as attributes of the
    newly defined class. This all happens when Config.__new__ is called.
    """
    
    def __init__(cls, name, bases, dict_):
        type.__init__(cls, name, bases, dict_)
        cls._fields = {}
        def getFields(classtype):
            fields = {}
            bases=list(classtype.__bases__)
            bases.reverse()
            # call getFields recursively to get attributes of sub-configs
            for b in bases:
                fields.update(getFields(b))

            # check each class attribute, and get those of type Field
            for k, v in classtype.__dict__.iteritems():
                if isinstance(v, Field):
                    fields[k] = v
            return fields

        fields = getFields(cls)
        
        # Check all fields and make them attributes in the Config class
        for k, v in fields.iteritems():
            v.name = k
            cls._fields[k] = v
            type.__setattr__(cls, k, v)

            
class Config(object):
    # Use the above metaclass to create this class
    __metaclass__ = ConfigMeta

    def __new__(cls, *args, **kw):
        name=kw.pop("__name", None)
        instance = object.__new__(cls)
        instance._name=name
        instance._storage = {}
        # load up defaults
        for field in instance._fields.itervalues():           
            field.__set__(instance, field.default)
        instance.update(**kw)
        return instance


    # __setstate__ and __getstate__ are used to pickle Config objects
    # This is needed by multiprocessing to run them in threads.
    # The actual Config code does this with a __reduce__ method and helper
    # function, but the principle is the same.
    def __setstate__(self, d):
        exec d['stream'] in {}, {'root': self}
        del d['stream']
    def __getstate__(self):
        stream = io.BytesIO()
        self.saveToStream(stream)
        return {'stream' : stream.getvalue() }
        
    def update(self, **kw):
        for name, value in kw.iteritems():            
            field = self._fields[name]
            field.__set__(self, value)

    def save(self, filename, root="root"):
        with open(filename, 'w') as outfile:
            self.saveToStream(outfile, root)
                
    def saveToStream(self, outfile, root="root"):
        """Write ourself in a form that can be used to re-create this object."""
        tmp = self._name
        self._rename(root)
        try:
            configType = type(self)
            typeString = _typeStr(configType)
            print >> outfile, "import %s" % (configType.__module__)
            print >> outfile, "assert type(%s)==%s, 'config is of type %%s.%%s" % (root, typeString), \
                "instead of %s' %% (type(root).__module__, type(root).__name__)" % (typeString,)
            self._save(outfile)
        finally:
            self._rename(tmp)
            
    def _save(self, outfile):
        for field in self._fields.itervalues():
            field.save(outfile, self)
        
    def _rename(self, name):
        self._name = name
        for field in self._fields.itervalues():
            field.rename(self)
        
    def __setattr__(self, attr, value):
        if attr in self._fields:
            self._fields[attr].__set__(self, value)
        elif attr in self.__dict__ or attr in ("_name", "_storage"):
            self.__dict__[attr] = value

