#!/usr/bin/env python

import argparse
import numpy
import lsst.daf.persistence as dafPersist
import lsst.meas.mosaic as measMosaic

def printMags(butler, dataId):
    """A simple function to print the RA and Dec, and magnitudes of sources
    """

    # load the sources
    sources  = butler.get('src', dataId)
    n = len(sources)
    
    # get the fluxes as numpy arrays.  For aperture fluxes, use getApFlux()
    flux, ferr = sources.getPsfFlux(),  sources.getPsfFluxErr()
    mag,  merr = 2.5*numpy.log10(flux), 2.5/numpy.log(10)*(ferr/flux)

    # get the zeropoint, and apply ubercal correction if available
    if butler.datasetExists('fcr_md', dataId):
        fcr_md     = butler.get("fcr_md", dataId)
        ffp        = measMosaic.FluxFitParams(fcr_md)
        x, y       = sources.getX(), sources.getY()
        correction = numpy.array([ffp.eval(x[i],y[i]) for i in range(n)])
        zeropoint  = 2.5*numpy.log10(fcr_md.get("FLUXMAG0")) + correction
    else:
        metadata   = butler.get('calexp_md', dataId)
        zeropoint  = 2.5*numpy.log10(metadata.get("FLUXMAG0"))

    mag = zeropoint - mag
    
    for i in range(n):
        print sources[i].getRa().asDegrees(), sources[i].getDec().asDegrees(), mag[i], merr[i]
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("root",  help="Root directory of dataset")
    parser.add_argument("visit", type=int, help="Visit to get")
    parser.add_argument("ccd",   type=int, help="CCD to get")
    parser.add_argument("-t", "--tract", default=0, help="Tract number if using ubercal")
    args = parser.parse_args()
    
    butler = dafPersist.Butler(args.root)
    dataId = {"visit" : args.visit, "ccd": args.ccd, 'tract':args.tract}
    
    printMags(butler, dataId)
