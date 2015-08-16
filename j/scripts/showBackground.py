#!/usr/bin/env python

import argparse
import numpy
import matplotlib.pyplot as pyplot
import lsst.daf.persistence as dafPersist

def main(rootDir, visit, ccd):

    # butler を開き読み込みたいデータの dataId を指定する
    butler = dafPersist.Butler(rootDir)
    dataId = {'visit': visit, 'ccd':ccd}

    # butler から一次処理済データデータを読み込む
    exposure = butler.get('calexp', dataId)

    # maskedImage で exposure を開き、画像を img という変数で読み込ませる
    mimg = exposure.getMaskedImage()
    img = mimg.getImage()

    # numpy ndarray に変換
    nimg = img.getArray()

    # 同じ過程を background データに対して実行
    bg = butler.get("calexpBackground", dataId)
    bgImg = bg.getImage().getArray()
    
    # array を arcsinh で伸ばして pyplot で png 画像の形式として保存
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
