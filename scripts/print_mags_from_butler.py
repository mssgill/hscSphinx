#!/usr/bin/env python

import argparse
import numpy
import lsst.daf.persistence as dafPersist


def printMags(butler, dataId):
    """A simple function to print the RA and Dec, and magnitudes of sources
    """

    # load the metadata
    metadata = butler.get('calexp_md', dataId)
    
    # load the sources
    sources  = butler.get('src', dataId)

    # get the fluxes as numpy arrays.  For aperture fluxes, use getApFlux()
    flux, ferr = sources.getPsfFlux(),  sources.getPsfFluxErr()
    mag,  merr = 2.5*numpy.log10(flux), 2.5/numpy.log(10)*(ferr/flux)

    zeropoint = 2.5*numpy.log10(metadata.get("FLUXMAG0"))
    
    for i in range(len(sources)):
        print sources[i].getRa().asDegrees(), sources[i].getDec().asDegrees(), zeropoint-mag[i], merr[i]
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("root",  help="Root directory of dataset")
    parser.add_argument("visit", type=int, help="Visit to get")
    parser.add_argument("ccd",   type=int, help="CCD to get")
    args = parser.parse_args()
    
    butler = dafPersist.Butler(args.root)
    dataId = {"visit" : args.visit, "ccd": args.ccd}
    
    printMags(butler, dataId)
