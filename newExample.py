#!/usr/bin/env python

import sys, os
import argparse

lang = {
    ".py" : "python",
    ".cc" : "C++",
    ".h"  : "C",
    ".c"  : "C",
    ".sql": "sql",
    ".sh" : "sh",
    ".csh": "csh",
    }

def main(infile):

    base = os.path.basename(infile)
    core, ext = os.path.splitext(base)

    tag = ".. _%s:\n" % (base)

    title = base + "\n"
    title += "-"*len(base) + "\n"

    down = "Download script :download:`%s`.\n"%(base)

    include = ".. literalinclude:: %s\n" % (base)
    include += "   :language: %s\n" % (lang.get(ext, "python"))

    print ""
    print tag
    print title
    print down
    print include

    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="Input example script")
    args = parser.parse_args()
    main(args.infile)
