
# original file in pipe_base:  python/lsst/pipe/base/argumentParser.py

import sys, os, re
import collections
import itertools
import argparse

        

def setDottedAttr(item, name, value):
    """Like setattr, but accepts hierarchical names, e.g. foo.bar.baz"""
    subitem = item
    subnameList = name.split(".")
    for subname in subnameList[:-1]:
        subitem = getattr(subitem, subname)
    setattr(subitem, subnameList[-1], value)


    
class DataIdContainer(object):
    """Container for DataId, e.g. {'visit': 0123, 'ccd': 10}

    This class does *not* fully reproduce the actual class functionality.
    A butler is used in the real DataIdContainer, but is not include here.
    """
    
    def __init__(self, level=None):
        self.datasetType = None
        self.level = level
        self.idList = []
        self.refList = []
        
    def makeDataRefList(self, namespace):

        # This simply appends dataId to the list rather than
        # obtaining a dataRef from the butler (butler is not shown here)
        for dataId in self.idList:
            dataRef = dataId              # normally call butler.subset()            
            self.refList.append(dataRef)   
        
class DataIdArgument(object):
    """Glorified struct for data about id arguments, used by ArgumentParser.add_id_argument"""
    
    def __init__(self, name, datasetType, ContainerClass=DataIdContainer):
        self.name = name
        self.datasetType = datasetType
        self.ContainerClass = ContainerClass


        
class ArgumentParser(argparse.ArgumentParser):
    """Derive from standard Python ArgumentParser to handle pipeline specific arguments. """
    
    def __init__(self, name, usage = "%(prog)s input [options]", **kwargs):
        self._name = name
        self._dataIdArgDict = {} # Dict of data identifier specifications, by argument name
        argparse.ArgumentParser.__init__(self, usage = usage, fromfile_prefix_chars = '@', epilog='',
                                         formatter_class = argparse.RawDescriptionHelpFormatter,**kwargs)

        # The actual ArgumentParser defines many arguemnts.  Here only '-c' and '-j' are shown
        self.add_argument(metavar="ROOT", dest="rawInput", help="path to input data repository")
        self.add_argument("-c", "--config", nargs="*", action=ConfigValueAction, metavar="NAME=VALUE",
                          help="config override(s), e.g. -c foo=newfoo bar.baz=3")
        self.add_argument("-j", "--processes", type=int, default=1, help="Number of processes to use")

    def add_id_argument(self, name, datasetType, help, ContainerClass=DataIdContainer):
        """A special method to add arguments which refer to DataIds used by the Pipeline """
        
        argName = name.lstrip("-")
        # The IdValueAction is definied below and parses args with form "--id visit=50^100..120:2"
        self.add_argument(name, nargs="*", action=IdValueAction, help=help, metavar="KEY=VALUE1[^VALUE2...]")
        dataIdArgument = DataIdArgument(name=argName, datasetType=datasetType, ContainerClass=ContainerClass)
        self._dataIdArgDict[argName] = dataIdArgument

    def parse_args(self, config, args=None):
        """Overload argparse.ArgumentParser's parse_args() method."""
        
        if args == None:
            args = sys.argv[1:]
        if len(args) < 1 or args[0].startswith("-") or args[0].startswith("@"):
            self.print_help()
            self.exit("%s: error: Must specify input as first argument" % self.prog)

        namespace = argparse.Namespace()
        namespace.input = os.path.abspath(args[0])
        namespace.config = config
        # Add data ID containers to namespace
        for dataIdArgument in self._dataIdArgDict.itervalues():
            setattr(namespace, dataIdArgument.name, dataIdArgument.ContainerClass())
        
        namespace = argparse.ArgumentParser.parse_args(self, args=args, namespace=namespace)

        self._processDataIds(namespace)
        return namespace

    def _processDataIds(self, namespace):
        for dataIdArgument in self._dataIdArgDict.itervalues():
            dataIdContainer = getattr(namespace, dataIdArgument.name)
            dataIdContainer.makeDataRefList(namespace)
        

        
class ConfigValueAction(argparse.Action):
    """argparse action callback to override config parameters using name=value pairs from command line"""
    def __call__(self, parser, namespace, values, option_string):
        """Override one or more config name value pairs"""

        if namespace.config is None:
            return
        for nameValue in values:
            name, sep, valueStr = nameValue.partition("=")
            if not valueStr:
                parser.error("%s value %s must be in form name=value" % (option_string, nameValue))
            # see if setting the string value works; if not, try eval
            try:
                setDottedAttr(namespace.config, name, valueStr)
            except AttributeError:
                parser.error("no config field: %s" % (name,))
            except Exception:
                value = eval(valueStr, {})
                setDottedAttr(namespace.config, name, value)

        
class IdValueAction(argparse.Action):
    """argparse action callback to process a data ID into a dict.

    The IdValueAction is used by argparse to handle our special DataId
    values with form "visit=50^100..120:2"
    """
    
    def __call__(self, parser, namespace, values, option_string):
        """Parse --id data and append results to namespace.<argument>.idList"""
        if namespace.config is None:
            return
        idDict = collections.OrderedDict()
        for nameValue in values:
            name, sep, valueStr = nameValue.partition("=")
            idDict[name] = []
            for v in valueStr.split("^"):
                mat = re.search(r"^(\d+)\.\.(\d+)(?::(\d+))?$", v)
                if mat:
                    v1 = int(mat.group(1))
                    v2 = int(mat.group(2))
                    v3 = mat.group(3); v3 = int(v3) if v3 else 1
                    for v in range(v1, v2 + 1, v3):
                        idDict[name].append(str(v))
                else:
                    idDict[name].append(v)
        keyList = idDict.keys()
        iterList = [idDict[key] for key in keyList]
        idDictList = [collections.OrderedDict(zip(keyList, valList))
            for valList in itertools.product(*iterList)]

        argName = option_string.lstrip("-")
        ident = getattr(namespace, argName)
        ident.idList += idDictList


        

        
