#!/usr/bin/env python

import argparse
import numpy
import matplotlib.pyplot as pyplot
import lsst.daf.persistence as dafPersist

def main(rootDir, visit, ccd):

    # make a butler and specify your dataId
    butler = dafPersist.Butler(rootDir)
    dataId = {'visit': visit, 'ccd':ccd}

    # get the exposure from the butler
    exposure = butler.get('calexp', dataId)

    # get the maskedImage from the exposure, and the image from the mimg
    mimg = exposure.getMaskedImage()
    img = mimg.getImage()

    # convert to a numpy ndarray
    nimg = img.getArray()

    # do the same for the background which has already been subtracted
    bg = butler.get("calexpBackground", dataId)
    bgImg = bg.getImage().getArray()
    
    # stretch it with arcsinh and make a png with pyplot
    fig, axes = pyplot.subplots(1, 3, sharex=True, sharey=True, figsize=(8,5))
    imgs   = nimg, bgImg, nimg+bgImg
    titles = "Image", "Background", "Img+Bg"
    for i in range(3):
        axes[i].imshow(numpy.arcsinh(imgs[i]), cmap='gray')
        axes[i].set_title(titles[i])
    pyplot.gcf().savefig("imgAndBg-%d-%d.png"%(visit,ccd))
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("root", help="Root directory of data repository")
    parser.add_argument("visit", type=int, help="Visit to show")
    parser.add_argument("ccd", type=int, help="CCD to show")
    args = parser.parse_args()
    
    main(args.root, args.visit, args.ccd)
