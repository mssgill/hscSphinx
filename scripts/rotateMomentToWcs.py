#!/usr/bin/env python

import math
import argparse
import numpy
import lsst.daf.persistence as dafPersist
import lsst.afw.geom as afwGeom
import lsst.afw.geom.ellipses as ellipses


def main(rootDir, visit, ccd, n=10):

    # make a butler and specify your dataId
    butler = dafPersist.Butler(rootDir)
    dataId = {'visit': visit, 'ccd':ccd}

    # get sources and wcs from the butler
    sources  = butler.get('src', dataId)
    exposure = butler.get('calexp', dataId, immediate=True)
    wcs      = exposure.getWcs()
    #trans    = wcs.getLinearTransform()
    pixScale = wcs.pixelScale().asArcseconds()
    
    for s in sources[:n]:

        # the transform commented-out above is for the whole CCD.  Let's use the local one
        trans = wcs.linearizePixelToSky(s.getCentroid(), afwGeom.arcseconds).getLinear()
        m0    = s.getShape()
        m_new = m0.transform(trans)

        # print before and after the transform as a sanity check
        ms  = m0, m_new
        pix = 1.0, pixScale
        for i in 0, 1:
            m = ms[i]
            ax = ellipses.Axes(m)
            # Ixx,yy,xy should be different after the transform
            print "%6.3f %6.3f %6.3f   " % (m.getIxx(), m.getIyy(), m.getIxy()),
            # but A,B should be the same since the transformed ones are divided by the pixelScale
            # --> untransformed theta is wrt x-axis and increases *counter-clockwise* (standard cartesian)
            # --> transformed theta   is wrt RA-axis and increases *clockwise*
            print "%6.3f %6.3f %6.3f   " % (ax.getA()/pix[i], ax.getB()/pix[i], ax.getTheta()),
        print ""
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("root", help="Root directory of data repository")
    parser.add_argument("visit", type=int, help="Visit to show")
    parser.add_argument("ccd", type=int, help="CCD to show")
    parser.add_argument("-n", "--number", type=int, default=10, help="Number of sources to print")
    args = parser.parse_args()
    
    main(args.root, args.visit, args.ccd, n=args.number)
