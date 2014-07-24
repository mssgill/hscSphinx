#!/usr/bin/env python

import math
import argparse
import numpy
import lsst.daf.persistence as dafPersist
import lsst.afw.geom as afwGeom
import lsst.afw.geom.ellipses as ellipses


def main(rootDir, visit, ccd, n=5):

    # make a butler and specify your dataId
    butler = dafPersist.Butler(rootDir)
    dataId = {'visit': visit, 'ccd':ccd}

    # the x,y of a galaxy, as if we're computing galaxy-galaxy shear about the object at this coordinate.
    gx, gy = 1000.0, 1000.0
    
    # get the exposure from the butler
    sources = butler.get('src', dataId)

    for s in sources[:n]:

        # get the shape and coords, and get the angle wrt x-axis
        moment = s.getShape()
        x, y   = s.getX(), s.getY()
        dx, dy = x - gx, y - gy
        angle  = -math.atan2(dy, dx)*afwGeom.radians

        # make a rotation transform and apply it to the shape (moment)
        rotation       = afwGeom.LinearTransform.makeRotation(angle)
        moment_rotated = moment.transform(rotation)

        # convert that to a 'Separable' of a specified type of ellipticity and radius
        # --> Ellipticities: Distortion, ReducedShear, ConformalShear
        # --> Radii:         DeterminantRadius, TraceRadius, LogDeterminantRadius, LogTraceRadius
        # Constructors have the form 'Separable<ellipticity><radius>()' ... e.g.
        separable_dd = ellipses.SeparableDistortionDeterminantRadius(moment_rotated)

        # extract the ellipticity from the 'Separable' object
        e_dis = separable_dd.getEllipticity()

        # convert to other ellipticity types if you wish
        e_red = ellipses.ReducedShear(e_dis)
        e_con = ellipses.ConformalShear(e_dis)

        # output all the different types
        # Here +/- E1 are tangential and radial, respectively
        for e in (e_dis, e_red, e_con):
            print "%6.3f %6.3f  " % (e.getE1(), e.getE2()),
        print ""
        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("root", help="Root directory of data repository")
    parser.add_argument("visit", type=int, help="Visit to show")
    parser.add_argument("ccd", type=int, help="CCD to show")
    parser.add_argument("-n", "--number", type=int, default=5, help="Number of sources to print")
    args = parser.parse_args()
    
    main(args.root, args.visit, args.ccd, n=args.number)
