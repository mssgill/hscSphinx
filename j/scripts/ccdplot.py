#!/usr/bin/env python

import argparse
import numpy
import matplotlib.pyplot as pyplot
import lsst.daf.persistence as dafPersist

def main(rootDir, visit, ccd):

    # butler を開き読み込みたいデータの dataId を指定する
    butler = dafPersist.Butler(rootDir)
    dataId = {'visit': visit, 'ccd':ccd}

    # butler から一次処理済データの exposure を抜き出す
    exposure = butler.get('calexp', dataId)

    # maskedImage で exposure を開き、画像を mimg という変数で読み込ませる
    mimg = exposure.getMaskedImage()
    img = mimg.getImage()

    # numpy ndarray に変換
    nimg = img.getArray()

    # array を arcsinh で伸ばして pyplot で png 画像の形式として保存
    pyplot.imshow(numpy.arcsinh(nimg), cmap='gray')
    pyplot.gcf().savefig("test.png")
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("root", help="Root directory of data repository")
    parser.add_argument("visit", type=int, help="Visit to show")
    parser.add_argument("ccd", type=int, help="CCD to show")
    args = parser.parse_args()
    
    main(args.root, args.visit, args.ccd)
