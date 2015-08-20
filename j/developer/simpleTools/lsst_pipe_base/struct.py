

class Struct(object):
    """A struct to which you can add any fields
    Intended for return values from run methods of Tasks, to provide easy but safe access.
    """
    def __init__(self, **keyArgs):
        """Create a Struct with the specified fields """
        object.__init__(self)
        for name, val in keyArgs.iteritems():
            self.__safeAdd(name, val)
    
    def __safeAdd(self, name, val):
        """Add a field; raise RuntimeError if it already exists or the name starts with __ """
        if hasattr(self, name):
            raise RuntimeError("Item %s already exists" % (name,))
        if name.startswith("__"):
            raise RuntimeError("Item name %r invalid; must not begin with __" % (name,))
        setattr(self, name, val)

    def __repr__(self):
        itemList = ["%s=%r" % (name, val) for name, val in self.getDict().iteritems()]
        return "%s(%s)" % (self.__class__.__name__, "; ".join(itemList))
