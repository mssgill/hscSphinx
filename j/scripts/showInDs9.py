#!/usr/bin/env python

import argparse
import lsst.daf.persistence  as dafPersist
import lsst.afw.image        as afwImage
import lsst.afw.display.ds9  as ds9

def main(rootDir, visit, ccd, frame=1, title="", scale="zscale", zoom="to fit", trans=60, useEllipse=False):

    # butler を開き読み込みたいデータの dataId を指定する
    butler = dafPersist.Butler(rootDir)
    dataId = {'visit': visit, 'ccd':ccd}

    # butler から一次処理済データを読み込む
    exposure = butler.get('calexp', dataId)

    # 読み込みたい天体情報を設定し、ds9.mtv() を読み込む
    settings = {'scale':scale, 'zoom': zoom, 'mask' : 'transparency %d' %(trans)}
    ds9.mtv(exposure, frame=frame, title=title, settings=settings)


    # 天体カタログを取得し、データ点を重ねて表示する

    sources = butler.get('src', dataId)

    with ds9.Buffering():
        for i,source in enumerate(sources):
            color = ds9.RED
            size = 5.0
            
            if useEllipse:
                # 楕円体のシンボルで表示
                symbol = "@:{ixx},{ixy},{iyy}".format(ixx=source.getIxx(),
                                                      ixy=source.getIxy(),
                                                      iyy=source.getIyy())
            else:
                # シンプルなシンボルで表示（例えば、 +, x, *, o が使える）
                symbol = "o"
                
            ds9.dot(symbol, source.getX(), source.getY(), ctype=color,
                    size=size, frame=frame, silent=True)
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("root", help="Root directory of data repository")
    parser.add_argument("visit", type=int, help="Visit to show")
    parser.add_argument("ccd", type=int, help="CCD to show")
    parser.add_argument("-e", "--useEllipse", action='store_true', help="Overplot ellipses")
    parser.add_argument("-f", "--frame", type=int, default=1, help="Frame")
    parser.add_argument("-s", "--scale", default="zscale", help="Gray-scale")
    parser.add_argument("-t", "--title", default="", help="Figure title")
    parser.add_argument("-T", "--trans", default=60, help="Transparency")
    parser.add_argument("-z", "--zoom",  default="to fit", help="Zoom")
    args = parser.parse_args()

    main(args.root, args.visit, args.ccd,
         frame=args.frame, title=args.title, scale=args.scale, zoom=args.zoom, trans=args.trans,
         useEllipse=args.useEllipse
     )
