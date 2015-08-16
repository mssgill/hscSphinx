#!/usr/bin/env python

import argparse
import numpy
import matplotlib.pyplot as pyplot
import lsst.daf.persistence as dafPersist

def main(rootDir, visit, ccd, n=5):

    # butler を開き読み込みたいデータの dataId を指定する
    butler = dafPersist.Butler(rootDir)
    dataId = {'visit': visit, 'ccd':ccd}

    # butler から一次処理済データのカタログファイルを抜き出す
    sources = butler.get('src', dataId)

    for src in sources[0:n]:
        
        # 天体の座標を取得する (ICRS coord)
        icrs      = src.get('coord')
        galactic  = icrs.toGalactic()
        fk5       = icrs.toFk5()
        ecliptic  = icrs.toEcliptic()

        # RA, Dec を取得する。ICRS と Fk5 で定義された形式のみ
        ra, dec    = icrs.getRa(),         icrs.getDec()
        
        # 関連する座標系のみ利用可能（つまり、fk5 の l, b の座標系へは変換できない）
        l, b       = galactic.getL(),      galactic.getB()
        ra2, dec2  = fk5.getRa(),          fk5.getDec()
        lamb, beta = ecliptic.getLambda(), ecliptic.getBeta()
        
        # 緯度, 経度を調べることができる。
        # icrs カタログに対して RA, Dec を返し、銀河系内の天体に対しては l, b を返す
        lon, lat   = icrs.getLongitude(),  icrs.getLatitude()

        sid = src.getId()

        print "ID: ", sid
        print "   ICRS        RA/Dec    (deg)", ra.asDegrees(), dec.asDegrees()
        print "   FK5         RA/Dec    (rad)", ra2.asRadians(), dec2.asRadians()
        print "   Galactic       l/b (arcmin)", l.asArcminutes(), b.asArcminutes()
        print "   Ecliptic lamb/beta (arcsec)", lamb.asArcseconds(), beta.asArcseconds()
        print "   Generic   Long/Lat    (str)", lon, lat
        
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("root", help="Root directory of data repository")
    parser.add_argument("visit", type=int, help="Visit to show")
    parser.add_argument("ccd", type=int, help="CCD to show")
    parser.add_argument("-n", "--number", type=int, default=5, help="Number of sources to print")
    args = parser.parse_args()
    
    main(args.root, args.visit, args.ccd, n=args.number)
