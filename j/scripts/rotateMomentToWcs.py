#!/usr/bin/env python

import math
import argparse
import numpy
import lsst.daf.persistence as dafPersist
import lsst.afw.geom as afwGeom
import lsst.afw.geom.ellipses as ellipses


def main(rootDir, visit, ccd, n=10):

    # butler を開き読み込みたいデータの dataId を指定する
    butler = dafPersist.Butler(rootDir)
    dataId = {'visit': visit, 'ccd':ccd}

    # butler から一次処理済データカタログと WCS データを読み込む
    sources  = butler.get('src', dataId)
    exposure = butler.get('calexp', dataId, immediate=True)
    wcs      = exposure.getWcs()
    #trans    = wcs.getLinearTransform()
    pixScale = wcs.pixelScale().asArcseconds()
    
    for s in sources[:n]:

        # 全 CCD に対し変換をコメントアウトする
        trans = wcs.linearizePixelToSky(s.getCentroid(), afwGeom.arcseconds).getLinear()
        m0    = s.getShape()
        m_new = m0.transform(trans)

        # 座標系の変換前・後のサニティーチェックを出力する
        ms  = m0, m_new
        pix = 1.0, pixScale
        for i in 0, 1:
            m = ms[i]
            ax = ellipses.Axes(m)
            # 座標変換後は Ixx, yy, xy は変わっているはず
            print "%6.3f %6.3f %6.3f   " % (m.getIxx(), m.getIyy(), m.getIxy()),
            # 変換された座標系は pixelScale で割られているため、A, B は同じはず
            # --> theta は x-軸 に対して無変換で、*反時計回り* に増加する（デカルト座標系）
            # --> theta は RA-軸 に対して変換され、*時計回り* に増加する
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
