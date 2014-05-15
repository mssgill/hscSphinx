#!/usr/bin/env python

import re
import argparse
import lsst.daf.persistence as dafPersist

def main(rootDir, visit, ccd, coadd):
    butler = dafPersist.Butler(rootDir)
    
    if coadd:
        dataId = {'tract':visit, 'patch': ccd, 'filter':'HSC-I'}
        get = "deepCoadd_src"
        label = "coadd"
    else:
        dataId = {'visit':visit, 'ccd': int(ccd)}
        get = "src"
        label = "sf"
    src = butler.get(get, dataId, immediate=True)
    
    lines =  str(src.schema).split("\n")

    nCharName = 36
    nCharType = 11
    nCharDoc  = 69

    fmt   = "%-"+str(nCharName) + "s  %-"+str(nCharType) + "s  %-"+str(nCharDoc)+"s\n"
    hline = fmt % ("="*nCharName, "="*nCharType, "="*nCharDoc)

    lookup = {
        "D": "Double",
        "L": "Long",
        "F": "Float",
        "I": "Int",
        }
    out = ""
    out += hline
    out += fmt % ("Name", "Type", "Doc")
    out += hline
    for line in lines:
        m = re.match(r'.*Field\[\'(.+?)\'\].*name\=\"(.+?)\", doc\=\"(.+?)\"', line)
        if not m:
            continue
        typ, name, doc = m.groups()
        if len(doc) > nCharDoc - 4:
            doc = doc[0:nCharDoc-4] + " ..."
        typ = lookup.get(typ, typ)
        out += fmt % (name, typ, doc)
    out += hline

    print out
    with open("prettySchema-"+label+".txt", 'w') as fp:
        fp.write(out)
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("root", help="Root directory of data repository")
    parser.add_argument("visit", type=int)
    parser.add_argument("ccd")
    parser.add_argument("-c", "--coadd", action='store_true', default=False)
    args = parser.parse_args()
    main(args.root, args.visit, args.ccd, args.coadd)
