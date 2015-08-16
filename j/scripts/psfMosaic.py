#!/usr/bin/env python

import argparse
import numpy
import matplotlib.pyplot      as pyplot
import lsst.daf.persistence   as dafPersist
import lsst.afw.geom          as afwGeom
import lsst.afw.image         as afwImage
import lsst.afw.display.utils as dispUtils
import lsst.afw.display.ds9   as ds9

def zscale(img, contrast=0.25, samples=500):

    ravel = img.ravel()
    if len(ravel) > samples:
        imsort = numpy.sort(numpy.random.choice(ravel, size=samples))
    else:
        imsort = numpy.sort(ravel)

    n = len(imsort)
    idx = numpy.arange(n)

    med = imsort[n/2]
    w = 0.25
    i_lo, i_hi = int((0.5-w)*n), int((0.5+w)*n)
    p = numpy.polyfit(idx[i_lo:i_hi], imsort[i_lo:i_hi], 1)
    slope, intercept = p

    z1 = med - (slope/contrast)*(n/2-n*w)
    z2 = med + (slope/contrast)*(n/2-n*w)

    return z1, z2
    

def main(rootDir, visit, ccd, n=4):

    # butler を開き読み込みたいデータの dataId を指定する
    butler = dafPersist.Butler(rootDir)
    dataId = {'visit': visit, 'ccd':ccd}

    # butler から一次処理済データのカタログファイルをとデータを読み込む
    sources = butler.get('src', dataId)
    exposure = butler.get("calexp", dataId)

    # calib.psf.used で flag がついている天体リストを作る
    psfSources = [s for s in sources if s.get("calib.psf.used")]

    wx, wy = 25, 25         # bounding box の大きさを指定

    subImages = []
    labels    = []
    for psfSrc in psfSources[0:n]:
        
        # この天体の bounding box を作る
        x, y = int(psfSrc.getX()), int(psfSrc.getY())
        bbox = afwGeom.Box2I(afwGeom.Point2I(x-wx/2, y-wy/2), afwGeom.Extent2I(wx, wy))

        # 新しい画像を作り、リストに加える
        subimg = afwImage.ImageF(exposure.getMaskedImage().getImage(), bbox)
        subImages.append(subimg)

        # ラベルつけのために ID を使う
        label = "ID="+str(psfSrc.getId())
        labels.append(label)


    # mosaic の天体を作り、仕様をセットする
    m = dispUtils.Mosaic()
    m.setGutter(2)          # 各 subimage の幅を指定する
    m.setBackground(0)
    m.setMode("square")

    # mosaic を作る
    mosaic = m.makeMosaic(subImages)

    # ds9 で表示し、その画像にラベルをつける
    ds9.mtv(mosaic)                
    m.drawLabels(labels)

    # pyplot で png 画像を作る（pyplot 用に y-軸 は判定居させている）
    img = mosaic.getArray()[::-1,:]
    vmin, vmax = zscale(img)
    pyplot.imshow(img, interpolation="none", cmap="gray", vmin=vmin, vmax=vmax)
    pyplot.gcf().savefig("mosaic.png")

    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("root", help="Root directory of data repository")
    parser.add_argument("visit", type=int, help="Visit to show")
    parser.add_argument("ccd", type=int, help="CCD to show")
    parser.add_argument("-n", "--number", type=int, default=4, help="Number of sources to show")
    args = parser.parse_args()
    
    main(args.root, args.visit, args.ccd, n=args.number)
