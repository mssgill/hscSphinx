

.. _findtract:

findTract.py
------------

This script creates class which inherits from CmdLineTask so that it
can be called like a regular pipeline script.  In this case, only a
short run() method is defined to get the central pixel coordinate for
dataRef and lookup the appropriate tract.

E.g. to get the tract for visit 1234, CCD 50 from ``myrerun`` in ``/path/to/data`` ::

    $ ./findTract.py /path/to/data --rerun=myrerun --id visit=1234 ccd=50

For a script this simple, you'd certainly be able to do write command
line interface yourself with argparse, and you could create your own
``butler`` to fetch the data.  But, by using the pipeline
``CmdLineTask`` you get these features by default, and you also gain
built-in parallel processing with the ``-j`` option.  With very little
effort, the script will run in the same way that all the pipeline
tools run.

The key points are to inherit from ``CmdLineTask``, and define a
``run()`` method which takes a ``dataRef``.  To use this new Task as a
script, be sure to include the final block which calls
``parseAndRun()``.  Otherwise, that's it!
    
::

    #!/usr/bin/env python
    import lsst.pipe.base      as pipeBase
    import lsst.afw.image      as afwImage
    import lsst.afw.cameraGeom as camGeom

    class FindTractTask(pipeBase.CmdLineTask):
        """A Task to find the tract associated with a visit/ccd. """

        def run(self, dataRef):

            calexp_md = dataRef.get("calexp_md")
            wcs    = afwImage.makeWcs(calexp_md)
            skymap = dataRef.get("deepCoadd_skyMap")

            # all this, just to get the center pixel coordinate
            camera = dataRef.get("camera")
            raft   = camGeom.cast_Raft(camera.findDetector(camGeom.Id(0)))
            detId  = camGeom.Id(calexp_md.get("DET-ID"))
            ccd    = camGeom.cast_Ccd(raft.findDetector(detId))
            size   = ccd.getSize().getPixels(ccd.getPixelSize())

            coord  = wcs.pixelToSky(size.getX()/2, size.getY()/2)
            tract  = skymap.findTract(coord).getId()

            d = dataRef.dataId
            print "%-6d %3d  %5d" % (d['visit'], d['ccd'], tract)
            return tract

    if __name__ == '__main__':
        FindTractTask.parseAndRun()


