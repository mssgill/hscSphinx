#!/usr/bin/env python

import argparse
import numpy
import matplotlib.pyplot as pyplot
import lsst.daf.persistence as dafPersist
import lsst.afw.geom.ellipses as geomEllip

def main(rootDir, visit, ccd, n=5):

    # butler を開き読み込みたいデータの dataId を指定する
    butler = dafPersist.Butler(rootDir)
    dataId = {'visit': visit, 'ccd':ccd}

    # butler から一次処理済データのカタログファイルを抜き出す
    sources = butler.get('src', dataId)

    for src in sources[0:n]:

        # adaptive moment を取得する
        m = src.get('shape.sdss')
        ixx, ixy, iyy = m.getIxx(), m.getIxy(), m.getIyy()

        # 楕円体に変換（theta はラジアン表記にする）
        e  = geomEllip.Axes(m)
        a, b, theta = e.getA(), e.getB(), e.getTheta()
        print ixx, ixy, iyy, "  ", a, b, theta

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("root", help="Root directory of data repository")
    parser.add_argument("visit", type=int, help="Visit to show")
    parser.add_argument("ccd", type=int, help="CCD to show")
    parser.add_argument("-n", "--number", type=int, default=5, help="Number of sources to print")
    args = parser.parse_args()
    
    main(args.root, args.visit, args.ccd, n=args.number)
