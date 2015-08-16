#!/usr/bin/env python

import numpy
import lsst.afw.geom  as afwGeom
import lsst.afw.table as afwTable

def writeFakeData():
    """id ra dec のカラムをもつ 2 つのテキストファイルを書く"""
    
    n = 20
    ra  = [10.0 + numpy.random.uniform(0.0, 1.0, n)]
    dec = [20.0 + numpy.random.uniform(0.0, 1.0, n)]
    ra.append(ra[0] + numpy.random.normal(0.0, (0.2*afwGeom.arcseconds).asDegrees(), n))
    dec.append(dec[0] + numpy.random.normal(0.0, (0.2*afwGeom.arcseconds).asDegrees(), n))

    id_offsets = 1000, 2000
    for i in 0, 1:
        filename = "coord{id}.dat".format(id=i+1)
        with open(filename, 'w') as fp:
            for i_p in range(n):
                out = "{id} {ra} {dec}\n".format(id=id_offsets[i]+i_p, ra=ra[i][i_p], dec=dec[i][i_p])
                fp.write(out)

                
def loadSourceCatalog(filename):
	"""ファイルを SourceCatalog に読み込む。カラム 1, 2, 3 が id, ra, dec となっている。"""
    
    schema = afwTable.SourceTable.makeMinimalSchema()
    table  = afwTable.SourceTable.make(schema)
    scat   = afwTable.SourceCatalog(table)

    with open(filename) as fp:
        for line in fp.readlines():
            id, ra, dec = line.split()
            s = scat.addNew()
            s.setId(int(id))
            s.setRa(float(ra)*afwGeom.degrees)
            s.setDec(float(dec)*afwGeom.degrees)
            
    return scat
    

    
def main():

    # 偽データを作る
    writeFakeData()

    # 偽データを読み込む
    scat1 = loadSourceCatalog("coord1.dat")
    scat2 = loadSourceCatalog("coord2.dat")
    
    # 偽データ 1, 2 をマッチさせる
    distance = 1.0*afwGeom.arcseconds
    matches = afwTable.matchRaDec(scat1, scat2, distance)    

    # マッチした id の列を表示する
    for match in matches:
        s1, s2, dist = match
        print s1.getId(), s2.getId(), (dist*afwGeom.radians).asArcseconds()
        
    
    
if __name__ == '__main__':
    main()
