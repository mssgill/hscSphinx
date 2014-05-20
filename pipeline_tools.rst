
==============
Pipeline Tools
==============

The HSC data reduction pipeline is built on a framework of software
tools which are under active development for the LSST pipeline.  For
those who are interested in working with data catalog information, the
HSC database is the best tool to use.  But for those who are
interested in working with HSC images, this toolkit provides the best
way to work with the data.  If you're familiar with running the
pipeline, the same EUPS 'setup' command you used to enable the
pipeline code will also enable the Application FrameWork ('afw') and
other pipeline tools.

::

    $ setup -v hscPipe <version>

The main pipeline tools you will like need to be concerned with are
the following:

#. The butler and dataRef: These are tools which can find and load
   various types of data for you. 
  
#. Exposures, MaskedImages, and Images: These are the various
   containers used to handle images. 

#. SourceCatalogs: These are containers for tabulated information about
   'sources', including things like coordinates, fluxes, adaptive
   moments, and their respective errors.

   
.. _tool_butler:
   
The Butler
----------

The butler is a data object used to find and retrieve data for you.
It can also store data for you, but as this tutorial is intended for
users working with pipeline outputs, we'd like to avoid the
possibility of a user accidentally overwriting data.  File permissions
should protect us from this, but we still request that you please stay
well away from writing operations.

The following will create a butler object::

    import lsst.daf.persistence as dafPersist
    # <snip> #
    dataDir = "/data/Subaru/HSC/rerun/myrerun"
    butler = dafPersist.Butler(dataDir)


The ``butler`` object can then be used to request data by calling the
``get()`` method with the keyword for the thing that you're requesting,
and the dataId for the data you're interested in.  Here's an example
where the dataId refers to a 'visit' and 'ccd'.  If you're working
with a coadd, then these would have to be changed to 'tract' and
'patch'::

    dataId = {'visit': 1234, 'ccd': 56}
    bias = butler.get('bias', dataId)

The '_filename' suffix
^^^^^^^^^^^^^^^^^^^^^^
    
If, instead of the actual data, you wanted to know the file from
which the data is being loaded, you can append ``_filename`` to the
target.  The example for the filename of the bias target, is::

    bias_filename = butler.get('bias_filename', dataId)

The '_md' (metadata) suffix
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Many of the butler targets have metadata associated with them.  If
you're interested only in the metadata, you can request it
specifically with an ``_md`` suffix on the target.  A common such
request is for ``calexp_md`` (for calibrated exposure)::

    calexp_md = butler.get("calexp_md", dataId)

.. _tool_dataref:
    
The dataRef
^^^^^^^^^^^
    
To use the butler, you need both the ``butler``, and the ``dataId``.
Alternatively, if you're working extensively with the same dataId, you
can obtain a butler 'data reference'.  Obtaining the same bias image
would then be done as follows::

    import hsc.pipe.base.butler as hscButler
    # <snip> #
    dataId = {'visit': 1234, 'ccd': 56}
    dataRef = hscButler.getDataRef(butler, dataId)
    bias = dataRef.get('bias')


Which you choose, depends on what you're trying to do.  If you're
manipulating data in a single script, it likely won't make any
difference.


Most popular butler targets
---------------------------

The butler can be used to ``get()`` just about any pipeline data
product you might be interested in.  The ones that are most likely to
be of interest to you are the following (parentheses show the data
type it will give you).

Calibration frames (require dataId with visit and ccd)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following are the main calibration data products.  All will return
image-based data in the form of an ``ExposureF``:

=========== =========== ================================
Target      Data type   Comment
=========== =========== ================================
**bias**    ExposureF   Bias image
**dark**    ExposureF   Dark current image (per second)
**flat**    ExposureF   Flat field image
**fringe**  ExposureF   Fringe image (prob. I-band only)
=========== =========== ================================


Single-Frame data (requires dataId with visit and ccd)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. **postISRCCD** (``ExposureF``): 'ISR' stands for 'instrument signature
   removal' (i.e. bias subtraction, flat fielding, fringe removal,
   etc).  The postISRCCD outputs are not written to disk by default.
   To enable writing these in a pipeline run, set
   ``isr.doWrite=True``.

#. **calexp** (``ExposureF``): This is a calibrated exposure.  This is
   essentially a postISRCCD with the background subtracted, and
   additional calibration-related metadata.  As postISRCCD isn't
   normally persisted (i.e. written to disk), this should be your
   go-to target for single-frame image data.

   
#. **psf** (``Psf``): This is the Psf used in image processing.  With it,
   you can reconstruct an image of the local PSF at any position in
   the frame for the dataId you request.  See ``Psf`` for information
   on how to use it.

#. **src** (``SourceCatalog``): This contains all measurements for all of
   the sources in the dataId requested, including such things as RA &
   Dec, flux (aperture, PSF, etc.), adaptive moments, and much (much
   much) more.

#. **wcs** and **fcr** (``ExposureI``): After single frame processing is
   complete, the ``mosaic`` process is used to create a self
   consistent re-calibration (i.e. an uber-calibration) for the
   astrometry and photometry.  The 'wcs' and 'fcr' targets contains
   the corrections for the astrometry and photometry, respectively.



Coadd data (requires dataId with tract and patch)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The values for the coadd data are the same as those for the single
frame data, but include the prefix ``deepCoadd_``.  There are no coadd
equivalents for the 'postISRCCD', 'wcs' and 'fcr' targets as these
apply only to single frame measurements.

==================== ===========================
Single Frame target  Coadd Target
==================== ===========================
calexp               **deepCoadd_calexp**
psf                  **deepCoadd_psf**
src                  **deepCoadd_src**
==================== ===========================


Finding other butler targets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If there's something specific that you're looking for, and you don't
know what it's called, the butler's cousin, called 'the mapper', has a
configuration file which contains all of the possible butler targets.
For the HSC camera, the mapper configuration can be found in the
``obs_subaru`` EUPS package.  The directory is therefore stored in the
environment variable ``$OBS_SUBARU_DIR`` (see :ref:`EUPS *_DIR
variables <back_eupsworks>`, and :ref:`.paf files <back_policy>`).
The file is::

    $ ls $OBS_SUBARU_DIR/policy/HscMapper.paf
    /data1a/ana/products2014/Linux64/obs_subaru/2.0.0/policy/HscMapper.paf

    
An Excerpt from the file looks like this::
    
    calexp: {
        template:      "%(pointing)05d/%(filter)s/corr/CORR-%(visit)07d-%(ccd)03d.fits"
        python:        "lsst.afw.image.ExposureF"
        persistable:   "ExposureF"
        storage:       "FitsStorage"
        level:         "Ccd"
        tables:        "raw"
        tables:        "raw_visit"
    }

This descripts a target called a 'calexp' (calibrated exposure).  The
``template`` indicates the directory tree relative to the root of your
data repository, ``python`` refers to the type of python class the
data will be loaded into, and the other fields are of importance only
to developers.  If you choose to look through the HscMapper.paf file
searching for a specific butler target, there's very little damage you
can do by simply loading a target to see what it is.  However, don't
ever attempt to edit the file yourself.



Exposures, MaskedImage, and Images
----------------------------------

``Exposure``, ``MaskedImage``, and ``Image`` are all used to handle
image-based data in the pipeline.  When used in python, the type is
also specified as a suffix.  It will usually be float 'F'
(e.g. ``ExposureF``) or integer 'I' (e.g. ``ImageI``).  An ``Image``
is the simplest one, containing only a 2D array of pixels; the
``MaskedImageF`` contains 3 separate ``Image`` objects (a data ImageF,
a mask ImageI, and a variance ImageF), and an ``ExposureF`` contains a
``MaskedImageF`` plus any metadata associated with it (i.e. what might
commonly be found in a FITS header).

In most cases, any image data you request from the butler will be
handed to you in the form of an ``ExposureF`` object.  In the form of
pipeline Image objects, these may be difficult to work with, but the
images can be converted to more familiar numpy images, if you're more
comfortable with that format.  In addition to the image data, the
associated metadata is also present in an object called a
``PropertySet``.  The following example demonstrates loading a
'calexp' with the butler and extracting both the image and metadata
information, and writing a PNG with matplotlib.  This would be used on
single-frame data (i.e. visit,ccd), while the 'deepCoadd_calexp'
butler target would be used for coadd data.


.. literalinclude:: scripts/ccdplot.py
   :language: python

    
SourceCatalogs
--------------

The output catalogs produced by the pipeline are stored in the form of
``SourceCatalogs``.  The ``SourceCatalog`` is an in-house data type
designed specifically for pipeline catalogs.  SourceCatalogs can be
thought of as tables with each rows containing an entry for a source,
and each column containing the values of a measurement for all
sources.  They can be obtained from the butler by requesting the 'src'
target (single-frame outputs) or 'deepCoadd_src' (coadd outputs)::

    sources = butler.get("src", dataId)
    
Values can be extracted by row and sometimes by column, depending on the type of the value.

* For values which are simple types (float, int, etc), you can obtain
   a ``numpy.ndarray`` containing **all** values of a measurement by
   calling ``sources.get('thing')`` , where 'thing' is a text label
   for the type of data you want, e.g. 'flux.aperture',
   'flux.aperture.err'.  These can be thought of as the columns of the
   SourceCatalog.  You can then use these in vector operations just as
   you would any ``numpy.ndarray``.  However, for more complicated
   types (e.g. 'coord'), ``SourceCatalog`` cannot be sliced along
   columns in this way.

* You can access individual sources by index (e.g. ``s = source[i]``),
   or by iterating in a loop (e.g. ``for src in sources``).  This will
   return a ``SourceRecord``, which is the entry containing all
   measurements made on a single source in the catalog.

This short example demonstrates both of these.  It get the number of
sources in the catalog for a dataId, and also the PSF flux as an
``ndarray``.  It then iterates through the sources, printing the PSF
flux and also extracting and printing 'classification.extendedness'
which is used for star-galaxy separation::


    # get a SourceCatalog from the butler
    sources = butler.get("src", dataId)

    # get the number of sources and an ndarray of PSF fluxes
    n = len(sources)
    psfFlux    = sources.get("flux.psf")

    # iterate over the sources, and also get 'extendedness' from each SourceRecord
    for i, src in enumerate(sources):
        print i, psfFlux[i], src.get("classification.extendedness")

        
Full listings for the current set of ``SourceCatalog`` fields are
shown for :ref:`Single-frame Schema <prettyschema_sf>`, and
:ref:`Coadd Schema <prettyschema_coadd>`.  Once you have a
SourceCatalog object, you can display a similar listing by directly
printing the ``schema`` member attribute::

    sources = butler.get("src", dataId)
    print sources.schema



Special data types in SourceRecords
-----------------------------------

SourceCatalogs contain a number of non-standard data types.

Coord and Angle
^^^^^^^^^^^^^^^

``Coord`` is used to store any type of celestial coordinate.  The
things it contains (R.A. and Dec, and transformed versions of them)
are angles and are themselves contained in a special data type
``Angle``.  Coord types include ICRS, FK5, Galactic, and Ecliptic.
Currently, ICRS and FK5 are actually the same thing.  Angles can be
accessed in any common angular format: degrees, radians, arcminutes,
and arcseconds.  The following demonstrates the basic usage

.. literalinclude:: scripts/print_coord.py
   :language: python


Moment
^^^^^^


Angle
^^^^^


Working with ds9
----------------

Displaying Images
^^^^^^^^^^^^^^^^^

The HSC pipeline code is also able to use ds9 to display images.  Ds9
is not included as a part of the pipeline software, so you'll have to
install it separately.  Once that's done, you can display any of the
image-based objects with the ``mtv()`` function::

    exposure = butler.get("calexp", dataId)
    ds9.mtv(exposure)

The more information you give ``mtv``, the more will be displayed.  If
display an Image, then only the image pixels will be shown.  However,
if you use a MaskedImage or Exposure, then the mask planes will be
show semi-transparently with different colors used to indicate
different mask bits being set.  The mask colors are currently the
following:

=================  =============
Mask Flag          Color
=================  =============
BAD                RED
CR                 MAGENTA
EDGE               YELLOW
INTERPOLATED       GREEN
SATURATED          GREEN
DETECTED           BLUE
DETECTED_NEGATIVE  CYAN
SUSPECT            YELLOW
=================  =============

    
The ``mtv()`` function supports additional parameters to configure
which frame the exposure is displayed on, its title, the ds9 'scale'
setting (grayscale), the zoom, and the mask transparency::

    settings = {'scale':'zscale', 'zoom': 'to fit', 'mask' : 'transparency 60'}
    ds9.mtv(exposure, frame=1, title="My Data", settings=settings)

A full example demonstrating loading an image with the butler, and
displaying to ds9 is included with the example scripts.  See
:ref:`showInDs9 <showInDs9>`.
